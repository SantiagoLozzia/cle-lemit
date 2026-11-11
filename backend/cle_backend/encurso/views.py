import json
import logging
import os
import subprocess
import tempfile
from datetime import date as date_type

from django.core.files.base import ContentFile
from django.db import transaction
from django.db.models import F
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render  # noqa: F401
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from weasyprint import HTML
import fitz
import base64 as b64lib
from datetime import datetime
from io import BytesIO

from cle_backend.permissions import (
    IsAdministracion,
    IsAdministracionOrDireccion,
    IsDireccion,
    IsAreaJefe,
    IsAreaUser,
    IsServiciosTecnologicos,
    PRIVILEGED_ROLES,
    get_user_rol,
    get_user_area,
    user_can_access_circuit,
    validate_upload_file,
    validate_editable_document,
)
from django.db.models import Q
from database.models import *
from .serializers import *

logger = logging.getLogger(__name__)


def _log(request, accion, descripcion, nro_circuito=None):
    EventoAuditoria.objects.create(
        usuario=request.user if request.user.is_authenticated else None,
        accion=accion,
        descripcion=descripcion,
        nro_circuito_id=nro_circuito,
    )

# Cargar la Tabla
class ObtenerTodoEnCurso(APIView):
    def get(self, request, format=None):
        rol = get_user_rol(request)

        servicios_en_curso = DataServicio.objects.filter(finalizado=False)

        if rol not in PRIVILEGED_ROLES:
            # Usuarios de área: solo ven su propia área + circuitos donde son inter-área
            user_area = get_user_area(request)
            presupuestos_area = Presupuesto.objects.filter(
                area_tematica=user_area
            ).values_list('nro_presupuesto', flat=True)
            interarea_circuitos = SolicitudInterarea.objects.filter(
                inter_areaTematica=user_area
            ).values_list('nro_circuito', flat=True)
            servicios_en_curso = servicios_en_curso.filter(
                Q(nro_presupuesto__in=presupuestos_area) |
                Q(nro_circuito__in=interarea_circuitos)
            )

        # Obtener el numero de presupuesto de los DataServicio
        numeros_presupuesto = servicios_en_curso.values_list('nro_presupuesto', flat=True)

        # Obtener el área temática de cada presupuesto y el nro_solicitante
        presupuestos = Presupuesto.objects.filter(nro_presupuesto__in=numeros_presupuesto).select_related('nro_solicitante')
        presupuesto_map = {presupuesto.nro_presupuesto: (presupuesto.area_tematica, presupuesto.nro_solicitante.nombre_solicitante, presupuesto.arancel_presupuesto) for presupuesto in presupuestos}

        # Serializar los datos de los DataServicio
        servicios_en_curso_serializer = DataServicioSerializer(servicios_en_curso, many=True)

        # Mapa de presupuestos adicionales por nro_dataServicio
        presupuestos_adicionales_map = {}
        for ds in servicios_en_curso.prefetch_related('presupuestos_adicionales'):
            presupuestos_adicionales_map[ds.nro_dataServicio] = [
                {'nro_presupuesto': p.nro_presupuesto, 'arancel_presupuesto': str(p.arancel_presupuesto)}
                for p in ds.presupuestos_adicionales.all()
            ]

        # Agregar los campos 'area_tematica', 'nombre_solicitante' y 'presupuestos_adicionales' a los datos de DataServicio
        for data_servicio in servicios_en_curso_serializer.data:
            nro_presupuesto = data_servicio['nro_presupuesto']
            area_tematica, nombre_solicitante, arancel_principal = presupuesto_map.get(nro_presupuesto, ('', '', 0))
            data_servicio['area_tematica'] = area_tematica
            data_servicio['nombre_solicitante'] = nombre_solicitante
            adicionales = presupuestos_adicionales_map.get(data_servicio['nro_dataServicio'], [])
            data_servicio['presupuestos_adicionales'] = adicionales
            total_arancel = float(arancel_principal) + sum(float(p['arancel_presupuesto']) for p in adicionales)
            data_servicio['total_arancel'] = total_arancel

        # Obtener el numero de circuito de los DataServicio
        numeros_circuito = servicios_en_curso.values_list('nro_circuito', flat=True)
        # circuitos = Circuito.objects.filter(nro_circuito__in=servicios_en_curso.values_list('nro_circuito', flat=True))

        # Obtener los datos de los otros modelos
        legajos = Legajo.objects.filter(nro_circuito__in=numeros_circuito)
        recepciones = Recepcion.objects.filter(nro_circuito__in=numeros_circuito)
        ordenes_servicio = OrdenServicio.objects.filter(nro_circuito__in=numeros_circuito)
        ciclos = CicloInforme.objects.filter(nro_circuito__in=numeros_circuito).prefetch_related('registros_ensayo', 'historial_correcciones')
        solicitudes_inter_area = SolicitudInterarea.objects.filter(nro_circuito__in=numeros_circuito)
        informes_inter_area = InformeInterarea.objects.filter(nro_circuito__in=numeros_circuito)
        nros_dataServicio = servicios_en_curso.values_list('nro_dataServicio', flat=True)
        nros_legajo = legajos.values_list('nro_legajo', flat=True)
        adjuntos_solicitud = AdjuntoSolicitudServicio.objects.filter(data_servicio__in=nros_dataServicio)
        adjuntos_factura = AdjuntoFactura.objects.filter(legajo__in=nros_legajo)

        # Mapa nro_legajo -> {count, total_monto} para calcular pendiente por DataServicio
        from decimal import Decimal as _Decimal
        factura_monto_map = {}
        for f in adjuntos_factura:
            entry = factura_monto_map.setdefault(f.legajo_id, {'count': 0, 'total': _Decimal('0')})
            entry['count'] += 1
            if f.monto:
                entry['total'] += f.monto
        # Mapa nro_circuito -> nro_legajo (usando valores serializados para consistencia de tipos)
        legajos_list = list(legajos.values('nro_legajo', 'nro_circuito'))
        circuito_legajo_map = {l['nro_circuito']: l['nro_legajo'] for l in legajos_list}

        # Segundo pass: agregar pendiente_factura a cada data_servicio (requiere los mapas anteriores)
        for data_servicio in servicios_en_curso_serializer.data:
            nro_circ = data_servicio['nro_circuito']
            nro_leg = circuito_legajo_map.get(nro_circ)
            factura_info = factura_monto_map.get(nro_leg) if nro_leg else None
            ta = data_servicio.get('total_arancel') or 0
            if nro_leg and ta > 0:
                if factura_info and factura_info['count'] > 0:
                    data_servicio['pendiente_factura'] = ta - float(factura_info['total'])
                else:
                    data_servicio['pendiente_factura'] = ta  # monto completo pendiente, aún sin facturas
            else:
                data_servicio['pendiente_factura'] = None

        # Serializar los datos
        legajos_serializer = LegajoEnCursoSerializer(legajos, many=True)
        recepciones_serializer = RecepcionEnCursoSerializer(recepciones, many=True)
        ordenes_servicio_serializer = OrdenServicioEnCursoSerializer(ordenes_servicio, many=True)
        ciclos_serializer = CicloInformeSerializer(ciclos, many=True)
        solicitudes_inter_area_serializer = SolicitudInterAreaEnCursoSerializer(solicitudes_inter_area, many=True)
        informes_inter_area_serializer = InformeInterAreaEnCursoSerializer(informes_inter_area, many=True)

        # Construir la respuesta
        response_data = {
            'solicitudes': servicios_en_curso_serializer.data,
            'legajos': legajos_serializer.data,
            'recepciones': recepciones_serializer.data,
            'ordenes_servicio': ordenes_servicio_serializer.data,
            'ciclos': ciclos_serializer.data,
            'solicitudes_inter_area': solicitudes_inter_area_serializer.data,
            'informes_inter_area': informes_inter_area_serializer.data,
            'adjuntos_solicitud': AdjuntoSolicitudServicioSerializer(adjuntos_solicitud, many=True).data,
            'adjuntos_factura': AdjuntoFacturaSerializer(adjuntos_factura, many=True).data,
        }

        # Devolver la respuesta
        return Response(response_data)

# Presupuesto
class NrosPresupuestoEnEspera(APIView):
    def get(self, request):
        # Filtrar los presupuestos con estado 'en_espera'
        numeros_presupuesto = Presupuesto.objects.filter(estado_presupuesto='en_espera') \
            .annotate(nombre_solicitante=F('nro_solicitante__nombre_solicitante')) \
            .values('nro_presupuesto', 'nombre_solicitante') \
            .order_by('nro_presupuesto')

        data = list(numeros_presupuesto)

        return Response(data)

def presupuestos_compatibles(request, nro_presupuesto):
    """Devuelve presupuestos en_espera con mismo solicitante y área temática que el presupuesto dado."""
    try:
        principal = Presupuesto.objects.select_related('nro_solicitante').get(nro_presupuesto=nro_presupuesto)
    except Presupuesto.DoesNotExist:
        return JsonResponse({'error': 'Presupuesto no encontrado.'}, status=404)
    compatibles = (
        Presupuesto.objects
        .filter(
            nro_solicitante=principal.nro_solicitante,
            area_tematica=principal.area_tematica,
            estado_presupuesto='en_espera',
        )
        .exclude(nro_presupuesto=nro_presupuesto)
        .values('nro_presupuesto', 'arancel_presupuesto')
        .order_by('nro_presupuesto')
    )
    data = [{'nro_presupuesto': p['nro_presupuesto'], 'arancel_presupuesto': str(p['arancel_presupuesto'])} for p in compatibles]
    return JsonResponse({'presupuestos': data}, status=200)


def presupuesto_seleccionado(request, nro_presupuesto):
    try:
        presupuesto = Presupuesto.objects.select_related('nro_solicitante').get(nro_presupuesto=nro_presupuesto)
        # Obtiene el nombre del solicitante asociado al presupuesto
        nombre_solicitante = presupuesto.nro_solicitante.nombre_solicitante
        
        # Construye el diccionario de datos a devolver
        data = {
            'nro_presupuesto': presupuesto.nro_presupuesto,
            'nombre_solicitante': nombre_solicitante,
            'arancel_presupuesto': str(presupuesto.arancel_presupuesto),
        }
        return JsonResponse(data)
    except Presupuesto.DoesNotExist:
        return JsonResponse({'error': 'Presupuesto no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Data Servicio
class CrearDataServicioView(APIView):
    def post(self, request, *args, **kwargs):
        # Crear una instancia de Circuito
        circuito_instance = Circuito.objects.create()

        # Crear una instancia de DataServicio utilizando la clave primaria del Circuito
        data_servicio_data = request.data
        data_servicio_data['nro_circuito'] = circuito_instance.pk
        data_servicio_serializer = DataServicioSerializer(data=data_servicio_data)

        if data_servicio_serializer.is_valid():
            data_servicio_instance = data_servicio_serializer.save()

            # Obtener el número de presupuesto del DataServicio
            nro_presupuesto = data_servicio_data.get('nro_presupuesto')

            # Actualizar el estado del presupuesto asociado
            try:
                presupuesto = Presupuesto.objects.get(nro_presupuesto=nro_presupuesto)
                presupuesto.estado_presupuesto = 'aceptado'
                presupuesto.save()
            except Presupuesto.DoesNotExist:
                pass  # Manejar el caso donde no se encuentra el presupuesto

            _log(request, 'crear_data_servicio',
                 f'Data servicio creado — circuito #{circuito_instance.pk}',
                 nro_circuito=circuito_instance.pk)
            return Response(data_servicio_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data_servicio_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def obtener_dataServicio(request, nro_dataServicio):
    try:
        # Obtener el objeto DataServicio
        data_servicio = DataServicio.objects.get(nro_dataServicio=nro_dataServicio)

        # Serializar el objeto DataServicio
        data_servicio_serializer = DataServicioSerializer(data_servicio)

        # Obtener el número de presupuesto asociado al DataServicio
        nro_presupuesto = data_servicio.nro_presupuesto.nro_presupuesto

        # Obtener el presupuesto asociado al DataServicio
        presupuesto = data_servicio.nro_presupuesto

        # Serializar el presupuesto
        presupuesto_serializer = PresupuestoSerializer(presupuesto)

        # Obtener el área temática y el arancel del presupuesto
        area_tematica = presupuesto_serializer.data['area_tematica']
        arancel_presupuesto = presupuesto_serializer.data['arancel_presupuesto']

        # Obtener el solicitante asociado al presupuesto
        solicitante = presupuesto.nro_solicitante

        # Serializar el solicitante
        solicitante_serializer = SolicitanteSerializer(solicitante)
        nombre_solicitante = solicitante_serializer.data['nombre_solicitante']

        # Construir el diccionario de respuesta
        response_data = {
            'nro_dataServicio': nro_dataServicio,
            'fecha_dataServicio': data_servicio_serializer.data['fecha_dataServicio'],
            'obra': data_servicio_serializer.data['obra'],
            'cant_numLabs' : data_servicio_serializer.data['cant_numLabs'],
            'plazo_estimado' : data_servicio_serializer.data['plazo_estimado'],
            'muestras' : data_servicio_serializer.data['muestras'],
            'nro_presupuesto' : nro_presupuesto,
            'area_tematica' : area_tematica,
            'nombre_solicitante' : nombre_solicitante,
            'arancel_presupuesto' : arancel_presupuesto,
            'observaciones' : data_servicio_serializer.data['observaciones']
        }

        return JsonResponse(response_data, status=200)
    except DataServicio.DoesNotExist:
        return JsonResponse({'error': 'El DataServicio no existe'}, status=404)
    except Exception:
        logger.exception("Error en obtener_dataServicio")
        return JsonResponse({'error': 'Error interno del servidor.'}, status=500)


def datos_facturacion(request, nro_dataServicio):
    try:
        from decimal import Decimal
        data_servicio = get_object_or_404(DataServicio, nro_dataServicio=nro_dataServicio)
        presupuesto = data_servicio.nro_presupuesto
        solicitante = presupuesto.nro_solicitante

        # Total: presupuesto principal + adicionales
        total = presupuesto.arancel_presupuesto
        for p in data_servicio.presupuestos_adicionales.all():
            total += p.arancel_presupuesto

        # Facturas
        legajo = Legajo.objects.filter(nro_circuito=data_servicio.nro_circuito).first()
        facturas = []
        total_facturado = Decimal('0')
        if legajo:
            for f in legajo.adjuntos_factura.all():
                facturas.append({
                    'id': f.id,
                    'fecha': f.fecha.strftime('%d/%m/%Y'),
                    'monto': str(f.monto) if f.monto is not None else None,
                    'archivo': f.archivo.name if f.archivo else None,
                })
                if f.monto:
                    total_facturado += f.monto

        pendiente = total - total_facturado

        return JsonResponse({
            'empresa': {
                'nro_solicitante': solicitante.nro_solicitante,
                'nombre': solicitante.nombre_solicitante,
                'cuit': solicitante.cuit,
                'direccion': solicitante.direccion,
                'localidad': solicitante.localidad,
                'provincia': solicitante.provincia,
                'telefono': solicitante.telefono,
                'email': solicitante.email,
            },
            'email_factura': data_servicio.email_factura,
            'email_informe_tecnico': data_servicio.email_informe_tecnico,
            'total_dataservicio': str(total),
            'facturas': facturas,
            'total_facturado': str(total_facturado),
            'pendiente': str(pendiente),
        }, status=200)
    except Exception:
        logger.exception("Error en datos_facturacion")
        return JsonResponse({'error': 'Error interno del servidor.'}, status=500)


class GuardarAdjuntoSolicitud(APIView):
    def post(self, request):
        nro_dataServicio = request.data.get('nroDataServicio')
        adjunto = request.FILES.get('archivo')
        try:
            validate_upload_file(adjunto)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        data_servicio = DataServicio.objects.get(nro_dataServicio=nro_dataServicio)
        AdjuntoSolicitudServicio.objects.create(data_servicio=data_servicio, archivo=adjunto)
        if not data_servicio.completo:
            data_servicio.completo = True
            data_servicio.save()
        return Response({'mensaje': 'Adjunto guardado.'}, status=status.HTTP_200_OK)

# Legajo
def obtener_rangoLab(request, nro_circuito):
    # Obtener la instancia de DataServicio correspondiente al nro_circuito
    dataservicio = get_object_or_404(DataServicio, nro_circuito=nro_circuito)

    # Obtener el objeto UltimoNumero para el año actual
    ultimo_numero_obj = UltimoNumero.obtener()

    # Obtener el último número actual
    ultimo_numero = ultimo_numero_obj.ultimo_numero_actual

    # Calcular el rango de laboratorios
    inicio_rango = ultimo_numero + 1
    cantidad_numeros = dataservicio.cant_numLabs
    final_rango = inicio_rango + cantidad_numeros - 1
    anio = timezone.now().year
    rangLab = f"{inicio_rango}-{final_rango}/{anio}"

    # Devolver la respuesta como JSON incluyendo el rangoLab y el último número
    response_data = {
        'rangoLab': rangLab,
        'ultimo_numero': final_rango
    }

    return JsonResponse(response_data)


class CrearLegajo(APIView):
    def post(self, request):
        # Obtener el número de circuito y el nuevo último número del request
        nro_circuito = request.data.get('nro_circuito')
        nuevo_ultimo_numero = request.data.get('nuevo_ultimo_numero')
        
        try:
            # Verificar si el circuito existe
            circuito_instance = Circuito.objects.get(nro_circuito=nro_circuito)

            # Crear los datos del legajo con la instancia de circuito
            legajo_data = request.data.copy()
            legajo_data['nro_circuito'] = circuito_instance.pk  # Clave primaria (ID) del circuito

            # Snapshot: capturar versión vigente del formulario al momento de creación
            if not legajo_data.get('version_formulario'):
                try:
                    config = ConfigFormulario.objects.get(tipo='legajo')
                    legajo_data['version_formulario'] = config.version_actual
                except ConfigFormulario.DoesNotExist:
                    legajo_data['version_formulario'] = '01'

            # Serializar los datos del legajo
            serializer = LegajoEnCursoSerializer(data=legajo_data)
            if serializer.is_valid():
                # Guardar el legajo
                serializer.save()
                
                # Actualizar el último número en el modelo UltimoNumero
                ultimo_numero_obj = UltimoNumero.obtener()
                ultimo_numero_obj.ultimo_numero_actual = nuevo_ultimo_numero
                ultimo_numero_obj.save()

                _log(request, 'crear_legajo',
                     f'Legajo creado — circuito #{nro_circuito}',
                     nro_circuito=int(nro_circuito) if nro_circuito else None)
                return Response({'message': 'Legajo creado y último número actualizado correctamente'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Circuito.DoesNotExist:
            return Response({'error': 'Circuito no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

def obtener_legajo(request, nro_circuito):
    try:
        # Buscar el nro_presupuesto en DataServicio
        data_servicio = DataServicio.objects.select_related('nro_presupuesto').get(nro_circuito=nro_circuito)
        nro_presupuesto = data_servicio.nro_presupuesto.nro_presupuesto
        
        presupuesto = Presupuesto.objects.select_related('nro_solicitante').get(nro_presupuesto=nro_presupuesto)
        # Obtiene el nombre del solicitante asociado al presupuesto
        nombre_solicitante = presupuesto.nro_solicitante.nombre_solicitante

        # Obtener los datos del Legajo
        legajo = Legajo.objects.get(nro_circuito=nro_circuito)
        nro_legajo = legajo.nro_legajo
        fecha_legajo = legajo.fecha_legajo
        rangos_laboratorios = legajo.rangos_laboratorios

        # Crear el diccionario de respuesta con los datos obtenidos
        response_data = {
            'nro_legajo': nro_legajo,
            'fecha_legajo': fecha_legajo,
            'rangos_laboratorios': rangos_laboratorios,
            'nombre_solicitante': nombre_solicitante,
            'version_formulario': legajo.version_formulario or '01',
        }

        print(type(response_data['fecha_legajo']))  # Debería mostrar <class 'datetime.date'>
        print(response_data['fecha_legajo'])  # Verifica el valor

        return JsonResponse(response_data, status=200)
    except DataServicio.DoesNotExist:
        return JsonResponse({'error': 'El DataServicio no existe'}, status=404)
    except Presupuesto.DoesNotExist:
        return JsonResponse({'error': 'El Presupuesto no existe'}, status=404)
    except Solicitante.DoesNotExist:
        return JsonResponse({'error': 'El Solicitante no existe'}, status=404)
    except Legajo.DoesNotExist:
        return JsonResponse({'error': 'El Legajo no existe'}, status=404)
    except Exception:
        logger.exception("Error en obtener_legajo")
        return JsonResponse({'error': 'Error interno del servidor.'}, status=500)

class GuardarAdjuntoFactura(APIView):
    permission_classes = [IsAuthenticated, IsAdministracion]

    def post(self, request):
        try:
            nro_legajo = request.data.get('nroLegajo')
            adjunto = request.FILES.get('archivo')
            nro_circuito = request.data.get('nroCircuito')

            validate_upload_file(adjunto)

            # Buscar la recepcion existente por nro_circuito
            recepcion_existente = Recepcion.objects.filter(nro_circuito_id=nro_circuito).first()

            if not recepcion_existente:
                # Si no existe, crear una nueva instancia de Recepcion
                circuito = get_object_or_404(Circuito, pk=nro_circuito)
                nueva_recepcion = Recepcion.objects.create(nro_circuito=circuito)

            # Guardar el adjunto en el nuevo modelo y marcar legajo como completo
            monto_raw = request.data.get('monto')
            monto = None
            if monto_raw not in (None, ''):
                try:
                    monto = float(monto_raw)
                except (ValueError, TypeError):
                    monto = None
            legajo = get_object_or_404(Legajo, nro_legajo=nro_legajo)
            AdjuntoFactura.objects.create(legajo=legajo, archivo=adjunto, monto=monto)
            if not legajo.completo:
                legajo.completo = True
                legajo.save()

            _log(request, 'subir_factura',
                 f'Factura subida al legajo #{nro_legajo} — circuito #{nro_circuito}',
                 nro_circuito=int(nro_circuito) if nro_circuito else None)
            return Response({'mensaje': 'Factura guardada.'}, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            logger.exception("Error en GuardarAdjuntoFactura")
            return Response({'error': 'Error interno del servidor.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GuardarPagoLegajo(APIView):
    def put(self, request, nro_circuito, *args, **kwargs):
        pago_nuevo = request.data.get('pago')  # Obtiene el pago del legajo del cuerpo de la solicitud

        # Buscar el legajo por nro_circuito
        try:
            legajo = Legajo.objects.get(nro_circuito=nro_circuito)
        except Legajo.DoesNotExist:
            # Si no se encuentra, devolver un mensaje de error
            return Response({'error': 'Legajo no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        # Actualizar el estado de recepción
        legajo.pago = pago_nuevo
        legajo.save()

        # Serializar la respuesta si es necesario
        serializer = GuardarPagoLegajoSerializer(legajo)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CambiarPlazoPago(APIView):
    def put(self, request, nro_circuito, *args, **kwargs):
        plazo_pago_nuevo = request.data.get('plazo_pago')  # Obtiene el nuevo plazo de pago del cuerpo de la solicitud

        # Buscar el Legajo por nro_circuito
        try:
            legajo = Legajo.objects.get(nro_circuito=nro_circuito)
        except Legajo.DoesNotExist:
            # Si no se encuentra, devolver un mensaje de error
            return Response({'error': 'Legajo no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        # Actualizar el estado de recepción
        legajo.plazo_pago = plazo_pago_nuevo
        legajo.save()

        # Serializar la respuesta si es necesario
        serializer = CambiarPlazoPagoSerializer(legajo)
        return Response(serializer.data, status=status.HTTP_200_OK)

def generar_pdf_legajo(request, nro_circuito):
    try:
        # Crear un request dummy con el parámetro nro_circuito
        dummy_request = HttpRequest()
        dummy_request.GET = {'nro_circuito': nro_circuito}
        
        # Obtener datos del legajo usando la función auxiliar
        legajo_response = obtener_legajo(dummy_request, nro_circuito)
        
        if legajo_response.status_code != 200:
            return legajo_response  # Devolver el error si la respuesta no es exitosa
        
        legajo_data = json.loads(legajo_response.content)  # Convertir el contenido JSON en dict
        
        # Preparar el contexto para la plantilla del PDF
        fecha_str = legajo_data.get('fecha_legajo')
        context = {
            'nro_legajo': legajo_data['nro_legajo'],
            'fecha_legajo': date_type.fromisoformat(fecha_str) if fecha_str else None,
            'rangos_laboratorios': legajo_data['rangos_laboratorios'],
            'nombre_solicitante': legajo_data['nombre_solicitante'],
        }

        # Renderizar la plantilla con los datos
        html_string = render_to_string('template_pdf_legajo.html', context)

        # Crear el objeto PDF
        pdf_file = HTML(string=html_string).write_pdf()

        # Preparar la respuesta HTTP para descargar el PDF
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="informe.pdf"'
        
        return response
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=404)
    except Exception:
        logger.exception("Error en generar_pdf_legajo")
        return JsonResponse({'error': 'Error interno del servidor.'}, status=500)


# Remito
class CambiarRemito(APIView):
    def put(self, request, nro_circuito, *args, **kwargs):
        remito_nuevo = request.data.get('nros_remitos')  # Obtiene el nuevo remito del cuerpo de la solicitud

        # Buscar la Recepcion por nro_circuito
        try:
            recepcion = Recepcion.objects.get(nro_circuito=nro_circuito)
        except Recepcion.DoesNotExist:
            # Si no se encuentra, crear una nueva Recepcion
            recepcion = Recepcion.objects.create(nro_circuito=nro_circuito, nros_remitos=remito_nuevo)
        
        # Actualizar el estado de recepción
        recepcion.nros_remitos = remito_nuevo
        recepcion.save()

        # Serializar la respuesta si es necesario
        serializer = CambiarRemitoSerializer(recepcion)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GuardarEstadoRecepcion(APIView):
    def put(self, request, nro_circuito, *args, **kwargs):
        estado_recepcion_nuevo = request.data.get('estado_recepcion')  # Obtiene el nuevo estado de recepción del cuerpo de la solicitud

        # Buscar la Recepcion por nro_circuito
        try:
            recepcion = Recepcion.objects.get(nro_circuito=nro_circuito)
        except Recepcion.DoesNotExist:
            # Si no se encuentra, crear una nueva Recepcion
            recepcion = Recepcion.objects.create(nro_circuito=nro_circuito, estado_recepcion=estado_recepcion_nuevo)
        
        # Actualizar el estado de recepción
        recepcion.estado_recepcion = estado_recepcion_nuevo
        recepcion.save()

        # Serializar la respuesta si es necesario
        serializer = GuardarEstadoMuestrasSerializer(recepcion)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CambiarPlazoMuestras(APIView):
    def put(self, request, nro_circuito, *args, **kwargs):
        plazo_muestras_nuevo = request.data.get('plazo_muestras')  # Obtiene el nuevo plazo de muestras del cuerpo de la solicitud

        # Buscar la Recepcion por nro_circuito
        try:
            recepcion = Recepcion.objects.get(nro_circuito=nro_circuito)
        except Recepcion.DoesNotExist:
            # Si no se encuentra, crear una nueva Recepcion
            recepcion = Recepcion.objects.create(nro_circuito=nro_circuito, plazo_muestras=plazo_muestras_nuevo)
        
        # Actualizar el estado de recepción
        recepcion.plazo_muestras = plazo_muestras_nuevo
        recepcion.save()

        # Serializar la respuesta si es necesario
        serializer = CambiarPlazoMuestrasSerializer(recepcion)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Orden de Servicio
class CrearOrdenServicio(APIView):
    def post(self, request, nro_circuito, *args, **kwargs):
        try:
            print(f"nro_circuito recibido: {nro_circuito}")  # Depuración
            # Obtener la instancia del modelo Circuito
            circuito = Circuito.objects.get(nro_circuito=nro_circuito)
            # Verificar si ya existe una Orden de Servicio con el mismo nro_circuito
            existe_orden = OrdenServicio.objects.filter(nro_circuito=circuito).exists()
            if existe_orden:
                return JsonResponse({'mensaje': 'Ya existe una Orden de Servicio con este número de circuito', 'nro_circuito': nro_circuito}, status=400)

            fecha_actual = timezone.now()
            try:
                config_os = ConfigFormulario.objects.get(tipo='orden_servicio')
                version_os = config_os.version_actual
            except ConfigFormulario.DoesNotExist:
                version_os = '01'
            nueva_instancia = OrdenServicio.objects.create(
                nro_circuito=circuito,
                fecha_ordenServicio=fecha_actual,
                observaciones='',
                completo=True,
                version_formulario=version_os,
            )
            return JsonResponse({'mensaje': 'Orden de servicio creada exitosamente', 'nro_circuito': nro_circuito}, status=201)
        except Circuito.DoesNotExist:
            return JsonResponse({'mensaje': 'Circuito no encontrado', 'nro_circuito': nro_circuito}, status=404)
        except Exception:
            logger.exception("Error en CrearOrdenServicio")
            return JsonResponse({'mensaje': 'Error al crear la orden de servicio.'}, status=400)

def preview_ordenservicio(request, nro_circuito):
    try:
        data_servicio = DataServicio.objects.select_related('nro_presupuesto').get(nro_circuito=nro_circuito)
        nro_presupuesto = data_servicio.nro_presupuesto.nro_presupuesto
        area_tematica = data_servicio.nro_presupuesto.area_tematica
        presupuesto = Presupuesto.objects.select_related('nro_solicitante').get(nro_presupuesto=nro_presupuesto)
        nombre_solicitante = presupuesto.nro_solicitante.nombre_solicitante
        plazo_estimado = data_servicio.plazo_estimado
        muestras = data_servicio.muestras
        legajo = Legajo.objects.get(nro_circuito=nro_circuito)
        nro_legajo = legajo.nro_legajo
        rangos_laboratorios = legajo.rangos_laboratorios
        detalle_presupuestos = DetallePresupuesto.objects.select_related('nro_servicio').filter(nro_presupuesto=nro_presupuesto)
        serializer = DetallePresupuestoSerializer(detalle_presupuestos, many=True)
        return JsonResponse({
            'fecha_ordenServicio': timezone.now().date(),
            'area_tematica': area_tematica,
            'nro_legajo': nro_legajo,
            'rangos_laboratorios': rangos_laboratorios,
            'plazo_estimado': plazo_estimado,
            'nombre_solicitante': nombre_solicitante,
            'servicio_solicitado': serializer.data,
            'muestras': muestras,
        }, status=200)
    except (DataServicio.DoesNotExist, Legajo.DoesNotExist, Presupuesto.DoesNotExist) as e:
        return JsonResponse({'error': str(e)}, status=404)
    except Exception:
        logger.exception("Error en preview_ordenservicio")
        return JsonResponse({'error': 'Error interno del servidor.'}, status=500)

def obtener_ordenServicio(request, nro_circuito):
    try:
        # Buscar el nro_presupuesto en DataServicio
        data_servicio = DataServicio.objects.select_related('nro_presupuesto').get(nro_circuito=nro_circuito)
        nro_presupuesto = data_servicio.nro_presupuesto.nro_presupuesto
        area_tematica = data_servicio.nro_presupuesto.area_tematica
        
        presupuesto = Presupuesto.objects.select_related('nro_solicitante').get(nro_presupuesto=nro_presupuesto)
        # Obtiene el nombre del solicitante asociado al presupuesto
        nombre_solicitante = presupuesto.nro_solicitante.nombre_solicitante

        # Obtener los datos del Data Servicio
        plazo_estimado = data_servicio.plazo_estimado
        muestras = data_servicio.muestras

        # Obtener los datos del Legajo
        legajo = Legajo.objects.get(nro_circuito=nro_circuito)
        nro_legajo = legajo.nro_legajo
        rangos_laboratorios = legajo.rangos_laboratorios

        # Obtener los datos de Orden Servicio
        orden_servicio = OrdenServicio.objects.get(nro_circuito=nro_circuito)
        nro_ordenServicio = orden_servicio.nro_ordenServicio
        fecha_ordenServicio = orden_servicio.fecha_ordenServicio
        observaciones = orden_servicio.observaciones

        # Obtener los detalles del presupuesto principal + adicionales
        def _detalles_presupuesto(nro_pres, es_adicional):
            detalles = DetallePresupuesto.objects.select_related('nro_servicio').filter(nro_presupuesto=nro_pres)
            return [
                {'nro_servicio': d.nro_servicio.nro_servicio, 'servicio': d.nro_servicio.servicio, 'cant': d.cant, 'es_adicional': es_adicional}
                for d in detalles
            ]

        servicio_solicitado = _detalles_presupuesto(nro_presupuesto, False)
        for pres_adicional in data_servicio.presupuestos_adicionales.all():
            detalles_adicionales = _detalles_presupuesto(pres_adicional.nro_presupuesto, True)
            if detalles_adicionales:
                servicio_solicitado += detalles_adicionales
            else:
                # El presupuesto adicional existe pero no tiene DetallePresupuesto; igualmente avisar al área
                servicio_solicitado.append({
                    'nro_servicio': pres_adicional.nro_presupuesto,
                    'servicio': f'Presupuesto adicional #{pres_adicional.nro_presupuesto} (sin detalle de servicios)',
                    'cant': '-',
                    'es_adicional': True,
                })

        # Crear el diccionario de respuesta con los datos obtenidos
        response_data = {
            'nro_ordenServicio': nro_ordenServicio,
            'fecha_ordenServicio': fecha_ordenServicio,
            'area_tematica': area_tematica,
            'nro_legajo': nro_legajo,
            'rangos_laboratorios': rangos_laboratorios,
            'nuevo_rango_lab': orden_servicio.nuevo_rango_lab,
            'plazo_estimado': plazo_estimado,
            'nombre_solicitante': nombre_solicitante,
            'servicio_solicitado': servicio_solicitado,
            'muestras': muestras,
            'observaciones': observaciones,
            'version_formulario': orden_servicio.version_formulario or '01',
        }

        return JsonResponse(response_data, status=200)
    except DataServicio.DoesNotExist:
        return JsonResponse({'error': 'El DataServicio no existe'}, status=404)
    except Presupuesto.DoesNotExist:
        return JsonResponse({'error': 'El Presupuesto no existe'}, status=404)
    except Solicitante.DoesNotExist:
        return JsonResponse({'error': 'El Solicitante no existe'}, status=404)
    except Legajo.DoesNotExist:
        return JsonResponse({'error': 'El Legajo no existe'}, status=404)
    except Exception:
        logger.exception("Error en obtener_ordenServicio")
        return JsonResponse({'error': 'Error interno del servidor.'}, status=500)

class CambiarPlazoEstimado(APIView):
    def put(self, request, nro_circuito, *args, **kwargs):
        plazo_estimado_nuevo = request.data.get('plazo_estimado')
        
        if not plazo_estimado_nuevo:
            return Response({'error': 'El plazo estimado es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener la instancia de Circuito
        circuito = get_object_or_404(Circuito, nro_circuito=nro_circuito)
        
        # Obtener la instancia de DataServicio utilizando la instancia de Circuito
        data_servicio = get_object_or_404(DataServicio, nro_circuito=circuito)
        
        try:
            # Actualizar el plazo estimado
            data_servicio.plazo_estimado = plazo_estimado_nuevo
            data_servicio.save()
            
            # Serializar la respuesta
            serializer = CambiarPlazoEstimadoSerializer(data_servicio)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            logger.exception("Error en CambiarPlazoEstimado")
            return Response({'error': 'Error interno del servidor.'}, status=status.HTTP_400_BAD_REQUEST)

# ── Ciclos de Informe ─────────────────────────────────────────────────────────

class CrearCiclo(APIView):
    permission_classes = [IsAuthenticated, IsAreaUser]

    def post(self, request, nro_circuito):
        if not user_can_access_circuit(request.user, nro_circuito):
            return Response({'error': 'No tiene permisos para este circuito.'}, status=status.HTTP_403_FORBIDDEN)
        circuito = get_object_or_404(Circuito, nro_circuito=nro_circuito)
        ultimo = CicloInforme.objects.filter(nro_circuito=circuito).order_by('-numero').first()
        numero = (ultimo.numero + 1) if ultimo else 1
        ciclo = CicloInforme.objects.create(nro_circuito=circuito, numero=numero)
        return Response(CicloInformeSerializer(ciclo).data, status=status.HTTP_201_CREATED)


class SubirInformeAreaCiclo(APIView):
    permission_classes = [IsAuthenticated, IsAreaUser]

    def post(self, request, ciclo_id):
        ciclo = get_object_or_404(CicloInforme, id=ciclo_id)
        if not user_can_access_circuit(request.user, ciclo.nro_circuito_id):
            return Response({'error': 'No tiene permisos para este circuito.'}, status=status.HTTP_403_FORBIDDEN)
        archivo = request.FILES.get('archivo')
        tipo = request.data.get('tipo', 'parcial')
        if not archivo:
            return Response({'error': 'Archivo requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_editable_document(archivo)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        ciclo.adjunto_informeArea = archivo
        ciclo.fecha_informeArea = timezone.now().date()
        ciclo.tipo = tipo
        if ciclo.rechazo_st_destino == 'area':
            ciclo.nota_rechazo_st = None
            ciclo.rechazo_st_destino = None
        ciclo.save()
        _log(request, 'subir_informe_area',
             f'Informe de área {tipo} #{ciclo.numero} subido — circuito #{ciclo.nro_circuito_id}',
             nro_circuito=ciclo.nro_circuito_id)
        return Response(CicloInformeSerializer(ciclo).data, status=status.HTTP_200_OK)


class SubirRegistroEnsayoCiclo(APIView):
    permission_classes = [IsAuthenticated, IsAreaUser]

    def post(self, request, ciclo_id):
        ciclo = get_object_or_404(CicloInforme, id=ciclo_id)
        if not user_can_access_circuit(request.user, ciclo.nro_circuito_id):
            return Response({'error': 'No tiene permisos para este circuito.'}, status=status.HTTP_403_FORBIDDEN)
        archivo = request.FILES.get('archivo')
        if not archivo:
            return Response({'error': 'Archivo requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        registro = RegistroEnsayoCiclo.objects.create(ciclo=ciclo, archivo=archivo)
        _log(request, 'subir_registro_ensayo',
             f'Registro de ensayo subido — ciclo {ciclo.tipo} #{ciclo.numero}, circuito #{ciclo.nro_circuito_id}',
             nro_circuito=ciclo.nro_circuito_id)
        return Response({'id': registro.id, 'archivo': str(registro.archivo)}, status=status.HTTP_201_CREATED)


class EliminarRegistroEnsayoCiclo(APIView):
    permission_classes = [IsAuthenticated, IsAreaUser]

    def delete(self, request, pk):
        registro = get_object_or_404(RegistroEnsayoCiclo, pk=pk)
        if not user_can_access_circuit(request.user, registro.ciclo.nro_circuito_id):
            return Response({'error': 'No tiene permisos.'}, status=status.HTTP_403_FORBIDDEN)
        ciclo = registro.ciclo
        registro.delete()
        _log(request, 'eliminar_registro_ensayo',
             f'Registro de ensayo eliminado — ciclo {ciclo.tipo} #{ciclo.numero}, circuito #{ciclo.nro_circuito_id}',
             nro_circuito=ciclo.nro_circuito_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class EliminarInformeAreaCiclo(APIView):
    permission_classes = [IsAuthenticated, IsAreaUser]

    def delete(self, request, ciclo_id):
        ciclo = get_object_or_404(CicloInforme, id=ciclo_id)
        if not user_can_access_circuit(request.user, ciclo.nro_circuito_id):
            return Response({'error': 'No tiene permisos.'}, status=status.HTTP_403_FORBIDDEN)
        if ciclo.firma_direccion:
            return Response({'error': 'No se puede eliminar un informe ya firmado.'}, status=status.HTTP_403_FORBIDDEN)
        ciclo.adjunto_informeArea = None
        ciclo.fecha_informeArea = None
        ciclo.tipo = 'parcial'
        ciclo.save()
        _log(request, 'eliminar_informe_area',
             f'Informe de área eliminado — ciclo #{ciclo.numero}, circuito #{ciclo.nro_circuito_id}',
             nro_circuito=ciclo.nro_circuito_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CambiarTipoCiclo(APIView):
    permission_classes = [IsAuthenticated, IsAreaUser]

    def patch(self, request, ciclo_id):
        ciclo = get_object_or_404(CicloInforme, id=ciclo_id)
        if not user_can_access_circuit(request.user, ciclo.nro_circuito_id):
            return Response({'error': 'No tiene permisos.'}, status=status.HTTP_403_FORBIDDEN)
        if ciclo.firma_direccion:
            return Response({'error': 'No se puede cambiar el tipo de un informe ya firmado.'}, status=status.HTTP_403_FORBIDDEN)
        if ciclo.adjunto_informeServicio:
            return Response({'error': 'No se puede cambiar el tipo: Administración ya subió el informe de servicio.'}, status=status.HTTP_403_FORBIDDEN)
        tipo = request.data.get('tipo')
        if tipo not in ['parcial', 'complementario', 'final']:
            return Response({'error': 'Tipo inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        ciclo.tipo = tipo
        ciclo.save()
        return Response(status=status.HTTP_200_OK)

# Inter Area
def obtener_servicios(request, nro_circuito):
    try:
        # Buscar el nro_presupuesto en DataServicio
        data_servicio = DataServicio.objects.select_related('nro_presupuesto').get(nro_circuito=nro_circuito)
        nro_presupuesto = data_servicio.nro_presupuesto.nro_presupuesto
        # area_tematica = data_servicio.nro_presupuesto.area_tematica
        
        # presupuesto = Presupuesto.objects.select_related('nro_solicitante').get(nro_presupuesto=nro_presupuesto)
        # # Obtiene el nombre del solicitante asociado al presupuesto
        # nombre_solicitante = presupuesto.nro_solicitante.nombre_solicitante

        # Obtener los detalles de Presupuesto y serializarlos
        detalle_presupuestos = DetallePresupuesto.objects.select_related('nro_servicio') \
                                                         .filter(nro_presupuesto=nro_presupuesto)
        serializer = DetallePresupuestoSerializer(detalle_presupuestos, many=True)
        servicio_solicitado = serializer.data

        # Crear el diccionario de respuesta con los datos obtenidos
        response_data = {
            # 'area_tematica': area_tematica,
            'servicio_solicitado': servicio_solicitado,
        }

        return JsonResponse(response_data, status=200)
    except DataServicio.DoesNotExist:
        return JsonResponse({'error': 'El DataServicio no existe'}, status=404)
    except Presupuesto.DoesNotExist:
        return JsonResponse({'error': 'El Presupuesto no existe'}, status=404)
    except Exception:
        logger.exception("Error en obtener_servicios")
        return JsonResponse({'error': 'Error interno del servidor.'}, status=500)

class CrearSolicitudInterarea(APIView):
    def post(self, request):
        # Obtener los datos de la solicitud desde el request
        data = request.data
        
        # Validar los datos recibidos
        serializer = SolicitudInterareaSerializer(data=data)
        
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    # Guardar la solicitud interarea
                    solicitud_interarea = serializer.save()

                    # Procesar los detalles de servicios_solicitudInterarea
                    detalles_interarea = data.get('servicios_solicitudInterarea', [])

                    for detalle_data in detalles_interarea:
                        nro_servicio_id = detalle_data.get('nro_servicio')
                        cant = detalle_data.get('cant')
                        
                        # Buscar y obtener la instancia del servicio
                        instancia_servicio = get_object_or_404(Servicio, nro_servicio=nro_servicio_id)
                        
                        # Crear una instancia de DetalleInterarea
                        DetalleInterarea.objects.create(
                            nro_solicitudInterarea=solicitud_interarea,
                            nro_servicio=instancia_servicio,
                            cant=cant
                        )
                    
                return Response({'message': 'Solicitud Interarea creada correctamente'}, status=status.HTTP_201_CREATED)
            except Exception:
                logger.exception("Error en CrearSolicitudInterarea")
                return Response({'error': 'Error interno del servidor.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def obtener_solicitudInterarea(request, nro_circuito):
    try:
        circuito = Circuito.objects.get(nro_circuito=nro_circuito)
        solicitudes = SolicitudInterarea.objects.filter(nro_circuito=circuito)
        result = []
        for solicitud in solicitudes:
            data = SolicitudInterareaSerializer(solicitud).data
            data['servicio_solicitado'] = DetalleInterareaSerializer(
                DetalleInterarea.objects.filter(nro_solicitudInterarea=solicitud), many=True
            ).data
            data['ciclos'] = CicloInterareaSerializer(
                CicloInterarea.objects.filter(nro_solicitudInterarea=solicitud), many=True
            ).data
            result.append(data)
        return JsonResponse(result, safe=False)
    except Circuito.DoesNotExist:
        return JsonResponse({'error': 'Circuito no encontrado'}, status=404)

class ConfirmarInterareaPrincipal(APIView):
    permission_classes = [IsAuthenticated, IsAreaJefe]

    def post(self, request, nro_solicitud):
        solicitud = get_object_or_404(SolicitudInterarea, pk=nro_solicitud)
        try:
            if request.user.userprofile.area_tematica != solicitud.areaTematica_origen:
                return Response({'error': 'Solo el área principal puede confirmar.'}, status=status.HTTP_403_FORBIDDEN)
        except AttributeError:
            return Response({'error': 'Sin permisos.'}, status=status.HTTP_403_FORBIDDEN)
        solicitud.confirmado_area_principal = True
        solicitud.comentario_rechazo_ap = None
        solicitud.save()
        _log(request, 'confirmar_interarea_principal',
             f'Área principal confirmó inter-área #{nro_solicitud}',
             nro_circuito=solicitud.nro_circuito_id)
        return Response(SolicitudInterareaSerializer(solicitud).data)


class RechazarInterareaPrincipal(APIView):
    permission_classes = [IsAuthenticated, IsAreaJefe]

    def post(self, request, nro_solicitud):
        solicitud = get_object_or_404(SolicitudInterarea, pk=nro_solicitud)
        try:
            if request.user.userprofile.area_tematica != solicitud.areaTematica_origen:
                return Response({'error': 'Solo el área principal puede rechazar.'}, status=status.HTTP_403_FORBIDDEN)
        except AttributeError:
            return Response({'error': 'Sin permisos.'}, status=status.HTTP_403_FORBIDDEN)
        comentario = request.data.get('comentario', '').strip()
        if not comentario:
            return Response({'error': 'Se requiere un comentario para rechazar.'}, status=status.HTTP_400_BAD_REQUEST)
        solicitud.confirmado_area_principal = False
        solicitud.comentario_rechazo_ap = comentario
        solicitud.save()
        _log(request, 'rechazar_interarea_principal',
             f'Área principal rechazó inter-área #{nro_solicitud}: {comentario}',
             nro_circuito=solicitud.nro_circuito_id)
        return Response(SolicitudInterareaSerializer(solicitud).data)


class GuardarAdjuntoInformeInterarea(APIView):
    permission_classes = [IsAuthenticated, IsAreaUser]

    def post(self, request):
        # Obtener datos del request
        archivo = request.FILES.get('archivo')
        nro_solicitudInterarea = request.data.get('nro_solicitudInterarea')
        nro_circuito = request.data.get('nro_circuito')

        try:
            validate_upload_file(archivo)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Buscar instancias de SolicitudInterarea y Circuito
            solicitud_interarea = SolicitudInterarea.objects.get(pk=nro_solicitudInterarea)
            if not user_can_manage_ciclo_ia(request.user, solicitud_interarea):
                return Response({'error': 'Solo el inter-área puede subir este informe.'}, status=status.HTTP_403_FORBIDDEN)
            circuito = Circuito.objects.get(pk=nro_circuito)

            # Crear instancia de InformeInterarea
            informe_interarea = InformeInterarea(
                fecha_informeInterarea=timezone.now().date(),
                adjunto_informeInterarea=archivo,
                nro_solicitudInterarea=solicitud_interarea,
                nro_circuito=circuito
            )
            informe_interarea.save()

            # Serializar la instancia creada
            serializer = InformeInterareaSerializer(informe_interarea)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except SolicitudInterarea.DoesNotExist:
            return Response({'error': 'Solicitud Interarea no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Circuito.DoesNotExist:
            return Response({'error': 'Circuito no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            logger.exception("Error en GuardarAdjuntoInformeInterarea")
            return Response({'error': 'Error interno del servidor.'}, status=status.HTTP_400_BAD_REQUEST)

# Eliminar adjuntos por ID
class EliminarAdjuntoSolicitud(APIView):
    def delete(self, request, pk):
        adjunto = get_object_or_404(AdjuntoSolicitudServicio, pk=pk)
        data_servicio = adjunto.data_servicio
        adjunto.delete()
        if not data_servicio.adjuntos.exists():
            data_servicio.completo = False
            data_servicio.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EliminarAdjuntoFactura(APIView):
    permission_classes = [IsAuthenticated, IsAdministracion]

    def delete(self, request, pk):
        adjunto = get_object_or_404(AdjuntoFactura, pk=pk)
        legajo = adjunto.legajo
        nro_circuito = legajo.nro_circuito_id
        adjunto.delete()
        if not legajo.adjuntos_factura.exists():
            legajo.completo = False
            legajo.save()
        _log(request, 'eliminar_factura',
             f'Factura eliminada del legajo #{legajo.nro_legajo} — circuito #{nro_circuito}',
             nro_circuito=nro_circuito)
        return Response(status=status.HTTP_204_NO_CONTENT)


class EliminarInformeInterarea(APIView):
    permission_classes = [IsAuthenticated, IsAreaUser]

    def delete(self, request, pk):
        informe = get_object_or_404(InformeInterarea, pk=pk)
        if not user_can_manage_ciclo_ia(request.user, informe.nro_solicitudInterarea):
            return Response({'error': 'No tiene permisos para eliminar este informe.'}, status=status.HTTP_403_FORBIDDEN)
        informe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EditarDataServicio(APIView):
    permission_classes = [IsAuthenticated, IsServiciosTecnologicos]

    def patch(self, request, nro_dataServicio):
        data_servicio = get_object_or_404(DataServicio, nro_dataServicio=nro_dataServicio)

        plazo_estimado = request.data.get('plazo_estimado')
        if plazo_estimado is not None:
            data_servicio.plazo_estimado = int(plazo_estimado)

        hubo_cambio_significativo = False

        cant_numLabs_nuevo = request.data.get('cant_numLabs')
        if cant_numLabs_nuevo is not None:
            cant_numLabs_nuevo = int(cant_numLabs_nuevo)
            if cant_numLabs_nuevo > data_servicio.cant_numLabs:
                delta = cant_numLabs_nuevo - data_servicio.cant_numLabs
                hubo_cambio_significativo = True
                try:
                    legajo = Legajo.objects.get(nro_circuito=data_servicio.nro_circuito)
                    legajo.labs_adicionales_pendientes += delta
                    legajo.save()
                except Legajo.DoesNotExist:
                    pass
            data_servicio.cant_numLabs = cant_numLabs_nuevo

        nro_presupuesto_adicional = request.data.get('nro_presupuesto_adicional')
        if nro_presupuesto_adicional:
            presupuesto = get_object_or_404(Presupuesto, nro_presupuesto=nro_presupuesto_adicional)
            data_servicio.presupuestos_adicionales.add(presupuesto)
            hubo_cambio_significativo = True
            # Avisar al admin que hay un monto adicional pendiente en el legajo
            try:
                legajo = Legajo.objects.get(nro_circuito=data_servicio.nro_circuito)
                legajo.monto_adicional_pendiente = True
                legajo.save()
            except Legajo.DoesNotExist:
                pass

        data_servicio.save()

        # Marcar la Orden de Servicio como modificada para que el área lo sepa
        if hubo_cambio_significativo:
            try:
                orden = OrdenServicio.objects.get(nro_circuito=data_servicio.nro_circuito)
                if orden.completo:
                    orden.modificada = True
                    orden.save()
            except Exception:
                logger.exception("Error al marcar OS como modificada en circuito %s", data_servicio.nro_circuito_id)

        return Response({'message': 'Data Servicio actualizado.'}, status=status.HTTP_200_OK)


class ConfirmarLecturaOS(APIView):
    def post(self, request, nro_circuito):
        try:
            orden = OrdenServicio.objects.get(nro_circuito=nro_circuito)
            orden.modificada = False
            orden.nuevo_rango_lab = ''
            orden.save()
            return Response({'ok': True}, status=status.HTTP_200_OK)
        except OrdenServicio.DoesNotExist:
            return Response({'error': 'Orden de servicio no encontrada.'}, status=status.HTTP_404_NOT_FOUND)


class AprobarLabsAdicionales(APIView):
    permission_classes = [IsAuthenticated, IsAdministracion]

    def post(self, request, nro_circuito):
        legajo = get_object_or_404(Legajo, nro_circuito=nro_circuito)
        cant_labs_nuevos = legajo.labs_adicionales_pendientes

        if cant_labs_nuevos <= 0 and not legajo.monto_adicional_pendiente:
            return Response({'error': 'No hay cambios pendientes.'}, status=status.HTTP_400_BAD_REQUEST)

        result = {}
        if cant_labs_nuevos > 0:
            ultimo_numero_obj = UltimoNumero.obtener()
            inicio_rango = ultimo_numero_obj.ultimo_numero_actual + 1
            final_rango = inicio_rango + cant_labs_nuevos - 1
            anio = timezone.now().year
            nuevo_rango = f"{inicio_rango}-{final_rango}/{anio}"

            legajo.rangos_laboratorios = f"{legajo.rangos_laboratorios}, {nuevo_rango}"
            legajo.labs_adicionales_pendientes = 0

            ultimo_numero_obj.ultimo_numero_actual = final_rango
            ultimo_numero_obj.save()

            result['nuevo_rango'] = nuevo_rango
            result['rangos_totales'] = legajo.rangos_laboratorios

            # Marcar la OS con el nuevo rango para que el área lo vea destacado
            try:
                orden = OrdenServicio.objects.get(nro_circuito=nro_circuito)
                orden.nuevo_rango_lab = nuevo_rango
                orden.modificada = True
                orden.save()
            except OrdenServicio.DoesNotExist:
                pass

        legajo.monto_adicional_pendiente = False
        legajo.save()

        return Response(result, status=status.HTTP_200_OK)


class SubirInformeServicioCiclo(APIView):
    permission_classes = [IsAuthenticated, IsAdministracionOrDireccion]

    def post(self, request, ciclo_id):
        ciclo = get_object_or_404(CicloInforme, id=ciclo_id)
        archivo = request.FILES.get('archivo')
        if not archivo:
            return Response({'error': 'Archivo requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_editable_document(archivo)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        ciclo.adjunto_informeServicio = archivo
        ciclo.fecha_informeServicio = timezone.now().date()
        ciclo.revision_confirmada = False
        ciclo.firma_responsable_area = False
        ciclo.firma_direccion = False
        ciclo.corregir = False
        ciclo.nota_rechazo_st = None
        ciclo.rechazo_st_destino = None
        ciclo.rechazo_area_destino = None
        ciclo.nota_rechazo_area = None
        ciclo.save()
        _log(request, 'subir_formato_institucional',
             f'Formato institucional subido — ciclo {ciclo.tipo} #{ciclo.numero}, circuito #{ciclo.nro_circuito_id}',
             nro_circuito=ciclo.nro_circuito_id)
        return Response(CicloInformeSerializer(ciclo).data, status=status.HTTP_200_OK)


@api_view(['GET'])
def obtener_correcciones_ciclo(request, ciclo_id):
    ciclo = get_object_or_404(CicloInforme, id=ciclo_id)
    return Response({'correcciones': ciclo.correcciones})


class AdvertirCorreccionesCiclo(APIView):
    def put(self, request, ciclo_id, *args, **kwargs):
        correcciones_nuevas = request.data.get('correcciones')
        if not correcciones_nuevas:
            return Response({'error': 'Las correcciones son requeridas.'}, status=status.HTTP_400_BAD_REQUEST)
        ciclo = get_object_or_404(CicloInforme, id=ciclo_id)
        try:
            ciclo.correcciones = correcciones_nuevas
            ciclo.corregir = True
            ciclo.revision_confirmada = False
            ciclo.save()
            return Response(AdvertirCorreccionesCicloSerializer(ciclo).data, status=status.HTTP_200_OK)
        except Exception:
            logger.exception("Error en AdvertirCorreccionesCiclo")
            return Response({'error': 'Error interno del servidor.'}, status=status.HTTP_400_BAD_REQUEST)


class CorregirCiclo(APIView):
    def put(self, request, ciclo_id, *args, **kwargs):
        ciclo = get_object_or_404(CicloInforme, id=ciclo_id)
        try:
            ciclo.corregir = False
            ciclo.save()
            return Response(CorregirCicloSerializer(ciclo).data, status=status.HTTP_200_OK)
        except Exception:
            logger.exception("Error en CorregirCiclo")
            return Response({'error': 'Error interno del servidor.'}, status=status.HTTP_400_BAD_REQUEST)


class ConfirmarRevisionCiclo(APIView):
    permission_classes = [IsAuthenticated, IsServiciosTecnologicos]

    def put(self, request, ciclo_id, *args, **kwargs):
        ciclo = get_object_or_404(CicloInforme, id=ciclo_id)
        ciclo.historial_correcciones.filter(estado='pendiente').update(estado='confirmada')
        ciclo.revision_confirmada = True
        ciclo.save()
        _log(request, 'confirmar_revision_st',
             f'Revisión ST confirmada — ciclo {ciclo.tipo} #{ciclo.numero}, circuito #{ciclo.nro_circuito_id}',
             nro_circuito=ciclo.nro_circuito_id)
        return JsonResponse({'message': 'Revisión confirmada correctamente.'})


class RechazarRevisionSTCiclo(APIView):
    permission_classes = [IsAuthenticated, IsServiciosTecnologicos]

    def put(self, request, ciclo_id):
        ciclo = get_object_or_404(CicloInforme, id=ciclo_id)
        destino = request.data.get('destino')
        nota = request.data.get('nota', '').strip()
        if destino not in ('administracion', 'area'):
            return Response({'error': 'Destino inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        if not nota:
            return Response({'error': 'La nota es requerida.'}, status=status.HTTP_400_BAD_REQUEST)
        ciclo.nota_rechazo_st = nota
        ciclo.rechazo_st_destino = destino
        ciclo.revision_confirmada = False
        if destino == 'administracion':
            if ciclo.adjunto_informeServicio_pdf:
                ciclo.adjunto_informeServicio_pdf.delete(save=False)
                ciclo.adjunto_informeServicio_pdf = None
            ciclo.pdf_confirmado_admin = False
        ciclo.save()
        Correccion.objects.create(
            ciclo=ciclo,
            tipo='st',
            destinatario=destino,
            descripcion=nota,
            autor=request.user,
        )
        _log(request, 'rechazar_revision_st',
             f'Revisión ST rechazada → {destino} — ciclo {ciclo.tipo} #{ciclo.numero}, circuito #{ciclo.nro_circuito_id}',
             nro_circuito=ciclo.nro_circuito_id)
        return Response(CicloInformeSerializer(ciclo).data, status=status.HTTP_200_OK)


class SubirInformeSTCorregido(APIView):
    permission_classes = [IsAuthenticated, IsServiciosTecnologicos]

    def post(self, request, ciclo_id):
        ciclo = get_object_or_404(CicloInforme, id=ciclo_id)
        archivo = request.FILES.get('archivo')
        if not archivo:
            return Response({'error': 'Archivo requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_editable_document(archivo)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        ciclo.adjunto_informeServicio = archivo
        ciclo.save()
        return Response(CicloInformeSerializer(ciclo).data, status=status.HTTP_200_OK)


def _convertir_docx_a_pdf_bytes(ruta_docx):
    """Convierte un docx a PDF usando LibreOffice headless. Retorna bytes del PDF."""
    with tempfile.TemporaryDirectory() as tmpdir:
        subprocess.run(
            [
                r'C:\Program Files\LibreOffice\program\soffice.exe',
                '--headless', '--convert-to', 'pdf',
                '--outdir', tmpdir,
                ruta_docx,
            ],
            timeout=60,
            check=True,
            capture_output=True,
        )
        nombre_base = os.path.splitext(os.path.basename(ruta_docx))[0]
        pdf_path = os.path.join(tmpdir, nombre_base + '.pdf')
        with open(pdf_path, 'rb') as f:
            return f.read()


class GenerarPDFServicioCiclo(APIView):
    permission_classes = [IsAuthenticated, IsAdministracion]

    def post(self, request, ciclo_id):
        ciclo = get_object_or_404(CicloInforme, id=ciclo_id)
        if not ciclo.adjunto_informeServicio:
            return Response({'error': 'No hay informe de servicio para convertir.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            pdf_bytes = _convertir_docx_a_pdf_bytes(ciclo.adjunto_informeServicio.path)
        except subprocess.CalledProcessError:
            return Response(
                {'error': 'Error al convertir el archivo. Verificá que LibreOffice esté instalado en el servidor.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except subprocess.TimeoutExpired:
            return Response({'error': 'Tiempo de conversión agotado.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if ciclo.adjunto_informeServicio_pdf:
            ciclo.adjunto_informeServicio_pdf.delete(save=False)

        nombre_base = os.path.splitext(os.path.basename(ciclo.adjunto_informeServicio.name))[0]
        ciclo.adjunto_informeServicio_pdf.save(
            f'{nombre_base}.pdf',
            ContentFile(pdf_bytes),
            save=False,
        )
        ciclo.pdf_confirmado_admin = True
        ciclo.save()
        _log(request, 'generar_pdf',
             f'PDF generado — ciclo {ciclo.tipo} #{ciclo.numero}, circuito #{ciclo.nro_circuito_id}',
             nro_circuito=ciclo.nro_circuito_id)
        return Response(CicloInformeSerializer(ciclo).data, status=status.HTTP_200_OK)


class RegistrarCorreccionST(APIView):
    permission_classes = [IsAuthenticated, IsServiciosTecnologicos]

    def post(self, request, ciclo_id):
        ciclo = get_object_or_404(CicloInforme, id=ciclo_id)
        descripcion = request.data.get('descripcion', '').strip()
        if not descripcion:
            return Response({'error': 'Descripción requerida.'}, status=status.HTTP_400_BAD_REQUEST)
        Correccion.objects.create(ciclo=ciclo, tipo='st', destinatario='administracion', descripcion=descripcion, autor=request.user)
        return Response(status=status.HTTP_201_CREATED)


class ConfirmarFirmaResponsableAreaCiclo(APIView):
    permission_classes = [IsAuthenticated, IsAreaJefe]

    def put(self, request, ciclo_id, *args, **kwargs):
        ciclo = get_object_or_404(CicloInforme, id=ciclo_id)
        if not user_can_access_circuit(request.user, ciclo.nro_circuito_id):
            return JsonResponse({'error': 'No tiene permisos para firmar este circuito.'}, status=403)

        # Obtener bytes de firma: primero del perfil, si no del canvas
        sig_bytes = None
        profile = getattr(request.user, 'userprofile', None)
        if profile and profile.firma:
            sig_bytes = profile.firma.read()
        else:
            firma_b64 = request.data.get('firma_imagen', '')
            if firma_b64:
                _, data = firma_b64.split(',', 1)
                sig_bytes = b64lib.b64decode(data)

        if sig_bytes and ciclo.adjunto_informeServicio_pdf:
            try:
                # Leer el PDF generado por Administración
                pdf_path = ciclo.adjunto_informeServicio_pdf.path
                doc = fitz.open(pdf_path)

                # Firma del área: imagen en TODAS las páginas
                for pg in doc:
                    pw, ph = pg.rect.width, pg.rect.height
                    sig_rect = fitz.Rect(15, ph - 150, 190, ph - 100)
                    pg.insert_image(sig_rect, stream=sig_bytes)

                # Leyenda solo en la última página
                page = doc[-1]
                pw, ph = page.rect.width, page.rect.height
                profile = getattr(request.user, 'userprofile', None)
                leyenda = (profile.leyenda.strip() if profile and profile.leyenda else '') or \
                          f"{request.user.first_name} {request.user.last_name}".strip() or \
                          request.user.username
                page.insert_textbox(
                    fitz.Rect(15, ph - 98, 190, ph - 72),
                    leyenda,
                    fontsize=7.5,
                    align=fitz.TEXT_ALIGN_CENTER,
                )

                buf = BytesIO()
                doc.save(buf)
                doc.close()
                buf.seek(0)

                # Guardar en campo separado, sin tocar el PDF de Admin
                import os
                original_name = os.path.basename(ciclo.adjunto_informeServicio_pdf.name)
                nombre_base, ext = os.path.splitext(original_name)
                from django.core.files.base import ContentFile
                ciclo.adjunto_firmado_area.save(
                    f"{nombre_base}_firmado_area{ext}",
                    ContentFile(buf.read()),
                    save=False,
                )
            except Exception:
                logger.exception("Error al insertar firma de área en PDF")

        ciclo.firma_responsable_area = True
        ciclo.save()
        _log(request, 'firma_responsable_area',
             f'Firma del responsable de área registrada — ciclo {ciclo.tipo} #{ciclo.numero}, circuito #{ciclo.nro_circuito_id}',
             nro_circuito=ciclo.nro_circuito_id)
        return JsonResponse({'message': 'Firma Responsable Area confirmada correctamente.'})


class ConfirmarFirmaDireccionCiclo(APIView):
    permission_classes = [IsAuthenticated, IsDireccion]

    def put(self, request, ciclo_id, *args, **kwargs):
        ciclo = get_object_or_404(CicloInforme, id=ciclo_id)

        try:
            legajo = Legajo.objects.get(nro_circuito=ciclo.nro_circuito)
            if str(legajo.pago) == 'pago_diferido':
                return Response(
                    {'error': 'No se puede firmar el informe mientras el pago figure como diferido. El circuito debe estar pagado al 100% primero.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Legajo.DoesNotExist:
            pass

        # Obtener bytes de firma: primero del perfil, si no del canvas
        sig_bytes = None
        profile = getattr(request.user, 'userprofile', None)
        if profile and profile.firma:
            sig_bytes = profile.firma.read()
        else:
            firma_b64 = request.data.get('firma_imagen', '')
            if firma_b64:
                _, data = firma_b64.split(',', 1)
                sig_bytes = b64lib.b64decode(data)

        # Base: PDF firmado por área si existe, sino el original de ST
        fuente = ciclo.adjunto_firmado_area or ciclo.adjunto_informeServicio
        if sig_bytes and fuente:
            try:
                doc = fitz.open(fuente.path)

                # Firma del director: solo en la última página, completa
                page = doc[-1]
                pw, ph = page.rect.width, page.rect.height

                sig_rect = fitz.Rect(pw - 190, ph - 150, pw - 15, ph - 100)
                page.insert_image(sig_rect, stream=sig_bytes)

                profile = getattr(request.user, 'userprofile', None)
                leyenda = (profile.leyenda.strip() if profile and profile.leyenda else '') or \
                          f"{request.user.first_name} {request.user.last_name}".strip() or \
                          request.user.username
                page.insert_textbox(
                    fitz.Rect(pw - 190, ph - 98, pw - 15, ph - 72),
                    leyenda,
                    fontsize=7.5,
                    align=fitz.TEXT_ALIGN_CENTER,
                )

                buf = BytesIO()
                doc.save(buf)
                doc.close()
                buf.seek(0)

                import os
                from django.core.files.base import ContentFile
                original_name = os.path.basename(fuente.name)
                nombre_base, _ = os.path.splitext(original_name)
                ciclo.adjunto_firmado_direccion.save(
                    f"{nombre_base}_firmado_dir.pdf",
                    ContentFile(buf.read()),
                    save=False,
                )
            except Exception:
                logger.exception("Error al insertar firma de dirección en PDF")

        ciclo.firma_direccion = True
        ciclo.save()
        _log(request, 'firma_direccion',
             f'Firma de Dirección registrada — ciclo {ciclo.tipo} #{ciclo.numero}, circuito #{ciclo.nro_circuito_id}',
             nro_circuito=ciclo.nro_circuito_id)
        return JsonResponse({'message': 'Firma Dirección confirmada correctamente.'})


class RechazarFirmaDireccionCiclo(APIView):
    permission_classes = [IsAuthenticated, IsDireccion]

    def put(self, request, ciclo_id, *args, **kwargs):
        ciclo = get_object_or_404(CicloInforme, id=ciclo_id)
        destino = request.data.get('destino', 'st')  # 'st', 'administracion' o 'area'
        nota = request.data.get('nota_rechazo', '')

        # Borrar PDF firmado por área y dirección
        if ciclo.adjunto_firmado_area:
            ciclo.adjunto_firmado_area.delete(save=False)
            ciclo.adjunto_firmado_area = None
        if ciclo.adjunto_firmado_direccion:
            ciclo.adjunto_firmado_direccion.delete(save=False)
            ciclo.adjunto_firmado_direccion = None

        # Borrar PDF de Administración (siempre que se rechace)
        if ciclo.adjunto_informeServicio_pdf:
            ciclo.adjunto_informeServicio_pdf.delete(save=False)
            ciclo.adjunto_informeServicio_pdf = None
        ciclo.pdf_confirmado_admin = False

        # Resetear firmas
        ciclo.firma_direccion = False
        ciclo.firma_responsable_area = False
        ciclo.revision_confirmada = False

        # Si vuelve al área, borrar también informe de servicio e informe de área
        if destino == 'area':
            if ciclo.adjunto_informeServicio:
                ciclo.adjunto_informeServicio.delete(save=False)
                ciclo.adjunto_informeServicio = None
            if ciclo.adjunto_informeArea:
                ciclo.adjunto_informeArea.delete(save=False)
                ciclo.adjunto_informeArea = None
            for registro in ciclo.registros_ensayo.all():
                registro.archivo.delete(save=False)
                registro.delete()

        # Guardar nota de rechazo y destino
        ciclo.nota_rechazo_direccion = nota
        ciclo.rechazo_destino = destino

        ciclo.save()
        if nota:
            Correccion.objects.create(
                ciclo=ciclo,
                tipo='direccion',
                destinatario=destino,
                descripcion=nota,
                autor=request.user,
            )
        _log(request, 'rechazar_firma_direccion',
             f'Firma de Dirección rechazada → {destino} — ciclo {ciclo.tipo} #{ciclo.numero}, circuito #{ciclo.nro_circuito_id}',
             nro_circuito=ciclo.nro_circuito_id)
        return JsonResponse({'message': 'Informe rechazado correctamente.'})


class RechazarFirmaResponsableAreaCiclo(APIView):
    permission_classes = [IsAuthenticated, IsAreaJefe]

    def put(self, request, ciclo_id, *args, **kwargs):
        ciclo = get_object_or_404(CicloInforme, id=ciclo_id)
        destino = request.data.get('destino', 'st')  # 'st', 'administracion' o 'area'
        nota = request.data.get('nota_rechazo', '')

        # Borrar PDF firmado por área y dirección
        if ciclo.adjunto_firmado_area:
            ciclo.adjunto_firmado_area.delete(save=False)
            ciclo.adjunto_firmado_area = None
        if ciclo.adjunto_firmado_direccion:
            ciclo.adjunto_firmado_direccion.delete(save=False)
            ciclo.adjunto_firmado_direccion = None

        # Borrar PDF de Administración (siempre que se rechace)
        if ciclo.adjunto_informeServicio_pdf:
            ciclo.adjunto_informeServicio_pdf.delete(save=False)
            ciclo.adjunto_informeServicio_pdf = None
        ciclo.pdf_confirmado_admin = False

        # Resetear firmas
        ciclo.firma_responsable_area = False
        ciclo.firma_direccion = False

        # Para todos los destinos: revision_confirmada=False para volver al paso del informe de servicio.
        # El adjunto_informeServicio nunca se borra aquí — siempre se conserva el trabajo de Admin/ST.
        ciclo.revision_confirmada = False

        # Guardar nota de rechazo de área
        ciclo.nota_rechazo_area = nota
        ciclo.rechazo_area_destino = destino

        # Limpiar nota de rechazo de dirección si la había
        ciclo.nota_rechazo_direccion = None
        ciclo.rechazo_destino = None

        ciclo.save()
        if nota:
            Correccion.objects.create(
                ciclo=ciclo,
                tipo='area',
                destinatario=destino,
                descripcion=nota,
                autor=request.user,
            )
        _log(request, 'rechazar_firma_area',
             f'Firma de Área rechazada → {destino} — ciclo {ciclo.tipo} #{ciclo.numero}, circuito #{ciclo.nro_circuito_id}',
             nro_circuito=ciclo.nro_circuito_id)
        return JsonResponse({'message': 'Informe rechazado por responsable de área correctamente.'})


# ── Ciclos de Informe Inter-Area ──────────────────────────────────────────────

def user_can_manage_ciclo_ia(user, solicitud):
    """Return True if the user is privileged or belongs to the inter_areaTematica."""
    try:
        rol = user.userprofile.rol
    except AttributeError:
        return False
    if rol in PRIVILEGED_ROLES:
        return True
    return user.userprofile.area_tematica == solicitud.inter_areaTematica


class CrearCicloIA(APIView):
    permission_classes = [IsAuthenticated, IsAreaUser]

    def post(self, request, nro_solicitud):
        solicitud = get_object_or_404(SolicitudInterarea, pk=nro_solicitud)
        if not user_can_manage_ciclo_ia(request.user, solicitud):
            return Response({'error': 'No tiene permisos para esta solicitud inter-area.'}, status=status.HTTP_403_FORBIDDEN)
        ultimo = CicloInterarea.objects.filter(nro_solicitudInterarea=solicitud).order_by('-numero').first()
        numero = (ultimo.numero + 1) if ultimo else 1
        ciclo_ia = CicloInterarea.objects.create(nro_solicitudInterarea=solicitud, numero=numero)
        _log(request, 'crear_ciclo_ia',
             f'Ciclo inter-area #{numero} creado — solicitudIA #{nro_solicitud}, circuito #{solicitud.nro_circuito_id}',
             nro_circuito=solicitud.nro_circuito_id)
        return Response(CicloInterareaSerializer(ciclo_ia).data, status=status.HTTP_201_CREATED)


class SubirInformeAreaCicloIA(APIView):
    permission_classes = [IsAuthenticated, IsAreaUser]

    def post(self, request, ciclo_id):
        ciclo_ia = get_object_or_404(CicloInterarea, pk=ciclo_id)
        solicitud = ciclo_ia.nro_solicitudInterarea
        if not user_can_manage_ciclo_ia(request.user, solicitud):
            return Response({'error': 'No tiene permisos para esta solicitud inter-area.'}, status=status.HTTP_403_FORBIDDEN)
        archivo = request.FILES.get('archivo')
        tipo = request.data.get('tipo', 'parcial')
        if not archivo:
            return Response({'error': 'Archivo requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_editable_document(archivo)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        ciclo_ia.adjunto_informeArea = archivo
        ciclo_ia.fecha_informeArea = timezone.now().date()
        ciclo_ia.tipo = tipo
        if ciclo_ia.rechazo_st_destino == 'area':
            ciclo_ia.nota_rechazo_st = None
            ciclo_ia.rechazo_st_destino = None
        ciclo_ia.save()
        # Si el área principal había rechazado, limpiar el rechazo al re-subir
        if solicitud.comentario_rechazo_ap:
            solicitud.comentario_rechazo_ap = None
            solicitud.confirmado_area_principal = False
            solicitud.save(update_fields=['comentario_rechazo_ap', 'confirmado_area_principal'])
        _log(request, 'subir_informe_area_ia',
             f'Informe de área inter-area #{ciclo_ia.numero} subido — solicitudIA #{solicitud.pk}, circuito #{solicitud.nro_circuito_id}',
             nro_circuito=solicitud.nro_circuito_id)
        return Response(CicloInterareaSerializer(ciclo_ia).data, status=status.HTTP_200_OK)


class SubirRegistroEnsayoCicloIA(APIView):
    permission_classes = [IsAuthenticated, IsAreaUser]

    def post(self, request, ciclo_id):
        ciclo_ia = get_object_or_404(CicloInterarea, pk=ciclo_id)
        solicitud = ciclo_ia.nro_solicitudInterarea
        if not user_can_manage_ciclo_ia(request.user, solicitud):
            return Response({'error': 'No tiene permisos.'}, status=status.HTTP_403_FORBIDDEN)
        archivo = request.FILES.get('archivo')
        if not archivo:
            return Response({'error': 'Archivo requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        registro = RegistroEnsayoCicloIA.objects.create(ciclo_ia=ciclo_ia, archivo=archivo)
        _log(request, 'subir_registro_ensayo_ia',
             f'Registro de ensayo inter-area subido — cicloIA #{ciclo_ia.numero}, circuito #{solicitud.nro_circuito_id}',
             nro_circuito=solicitud.nro_circuito_id)
        return Response({'id': registro.id, 'archivo': str(registro.archivo)}, status=status.HTTP_201_CREATED)


class EliminarRegistroEnsayoCicloIA(APIView):
    permission_classes = [IsAuthenticated, IsAreaUser]

    def delete(self, request, pk):
        registro = get_object_or_404(RegistroEnsayoCicloIA, pk=pk)
        solicitud = registro.ciclo_ia.nro_solicitudInterarea
        if not user_can_manage_ciclo_ia(request.user, solicitud):
            return Response({'error': 'No tiene permisos.'}, status=status.HTTP_403_FORBIDDEN)
        ciclo_ia = registro.ciclo_ia
        registro.delete()
        _log(request, 'eliminar_registro_ensayo_ia',
             f'Registro de ensayo inter-area eliminado — cicloIA #{ciclo_ia.numero}, circuito #{solicitud.nro_circuito_id}',
             nro_circuito=solicitud.nro_circuito_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubirInformeServicioCicloIA(APIView):
    permission_classes = [IsAuthenticated, IsAdministracion]

    def post(self, request, ciclo_id):
        ciclo_ia = get_object_or_404(CicloInterarea, pk=ciclo_id)
        archivo = request.FILES.get('archivo')
        if not archivo:
            return Response({'error': 'Archivo requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_editable_document(archivo)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        ciclo_ia.adjunto_informeServicio = archivo
        ciclo_ia.fecha_informeServicio = timezone.now().date()
        ciclo_ia.save()
        solicitud = ciclo_ia.nro_solicitudInterarea
        _log(request, 'subir_informe_servicio_ia',
             f'Informe de servicio inter-area #{ciclo_ia.numero} subido — circuito #{solicitud.nro_circuito_id}',
             nro_circuito=solicitud.nro_circuito_id)
        return Response(CicloInterareaSerializer(ciclo_ia).data, status=status.HTTP_200_OK)


class GenerarPDFCicloIA(APIView):
    permission_classes = [IsAuthenticated, IsAdministracion]

    def post(self, request, ciclo_id):
        ciclo_ia = get_object_or_404(CicloInterarea, pk=ciclo_id)
        if not ciclo_ia.adjunto_informeServicio:
            return Response({'error': 'No hay informe de servicio para convertir.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            pdf_bytes = _convertir_docx_a_pdf_bytes(ciclo_ia.adjunto_informeServicio.path)
        except subprocess.CalledProcessError:
            return Response(
                {'error': 'Error al convertir el archivo. Verificá que LibreOffice esté instalado en el servidor.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except subprocess.TimeoutExpired:
            return Response({'error': 'Tiempo de conversión agotado.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if ciclo_ia.adjunto_informeServicio_pdf:
            ciclo_ia.adjunto_informeServicio_pdf.delete(save=False)

        nombre_base = os.path.splitext(os.path.basename(ciclo_ia.adjunto_informeServicio.name))[0]
        ciclo_ia.adjunto_informeServicio_pdf.save(
            f'{nombre_base}.pdf',
            ContentFile(pdf_bytes),
            save=False,
        )
        ciclo_ia.pdf_confirmado_admin = True
        ciclo_ia.save()
        solicitud = ciclo_ia.nro_solicitudInterarea
        _log(request, 'generar_pdf_ia',
             f'PDF inter-area generado — cicloIA #{ciclo_ia.numero}, circuito #{solicitud.nro_circuito_id}',
             nro_circuito=solicitud.nro_circuito_id)
        return Response(CicloInterareaSerializer(ciclo_ia).data, status=status.HTTP_200_OK)


class AdvertirCorreccionesCicloIA(APIView):
    def put(self, request, ciclo_id):
        correcciones_nuevas = request.data.get('correcciones')
        if not correcciones_nuevas:
            return Response({'error': 'Las correcciones son requeridas.'}, status=status.HTTP_400_BAD_REQUEST)
        ciclo_ia = get_object_or_404(CicloInterarea, pk=ciclo_id)
        ciclo_ia.correcciones = correcciones_nuevas
        ciclo_ia.corregir = True
        ciclo_ia.revision_confirmada = False
        ciclo_ia.save()
        return Response(CicloInterareaSerializer(ciclo_ia).data, status=status.HTTP_200_OK)


class CorregirCicloIA(APIView):
    def put(self, request, ciclo_id):
        ciclo_ia = get_object_or_404(CicloInterarea, pk=ciclo_id)
        ciclo_ia.corregir = False
        ciclo_ia.save()
        return Response(CicloInterareaSerializer(ciclo_ia).data, status=status.HTTP_200_OK)


class ConfirmarRevisionCicloIA(APIView):
    permission_classes = [IsAuthenticated, IsServiciosTecnologicos]

    def put(self, request, ciclo_id):
        ciclo_ia = get_object_or_404(CicloInterarea, pk=ciclo_id)
        ciclo_ia.historial_correcciones.filter(estado='pendiente').update(estado='confirmada')
        ciclo_ia.revision_confirmada = True
        ciclo_ia.save()
        solicitud = ciclo_ia.nro_solicitudInterarea
        _log(request, 'confirmar_revision_ia',
             f'Revisión ST confirmada — cicloIA #{ciclo_ia.numero}, circuito #{solicitud.nro_circuito_id}',
             nro_circuito=solicitud.nro_circuito_id)
        return JsonResponse({'message': 'Revisión inter-area confirmada correctamente.'})


class RechazarRevisionSTCicloIA(APIView):
    permission_classes = [IsAuthenticated, IsServiciosTecnologicos]

    def put(self, request, ciclo_id):
        ciclo_ia = get_object_or_404(CicloInterarea, pk=ciclo_id)
        destino = request.data.get('destino')
        nota = request.data.get('nota', '').strip()
        if destino not in ('administracion', 'area'):
            return Response({'error': 'Destino inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        if not nota:
            return Response({'error': 'La nota es requerida.'}, status=status.HTTP_400_BAD_REQUEST)
        ciclo_ia.nota_rechazo_st = nota
        ciclo_ia.rechazo_st_destino = destino
        ciclo_ia.revision_confirmada = False
        if destino == 'administracion':
            if ciclo_ia.adjunto_informeServicio_pdf:
                ciclo_ia.adjunto_informeServicio_pdf.delete(save=False)
                ciclo_ia.adjunto_informeServicio_pdf = None
            ciclo_ia.pdf_confirmado_admin = False
        ciclo_ia.save()
        CorreccionIA.objects.create(
            ciclo_ia=ciclo_ia,
            tipo='st',
            destinatario=destino,
            descripcion=nota,
            autor=request.user,
        )
        solicitud = ciclo_ia.nro_solicitudInterarea
        _log(request, 'rechazar_revision_st_ia',
             f'Revisión ST inter-area rechazada → {destino} — cicloIA #{ciclo_ia.numero}, circuito #{solicitud.nro_circuito_id}',
             nro_circuito=solicitud.nro_circuito_id)
        return Response(CicloInterareaSerializer(ciclo_ia).data, status=status.HTTP_200_OK)


class SubirInformeSTCorregidoCicloIA(APIView):
    permission_classes = [IsAuthenticated, IsServiciosTecnologicos]

    def post(self, request, ciclo_id):
        ciclo_ia = get_object_or_404(CicloInterarea, pk=ciclo_id)
        archivo = request.FILES.get('archivo')
        if not archivo:
            return Response({'error': 'Archivo requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_editable_document(archivo)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        ciclo_ia.adjunto_informeServicio = archivo
        ciclo_ia.save()
        return Response(CicloInterareaSerializer(ciclo_ia).data, status=status.HTTP_200_OK)


class ConfirmarFirmaResponsableAreaCicloIA(APIView):
    permission_classes = [IsAuthenticated, IsAreaJefe]

    def put(self, request, ciclo_id):
        ciclo_ia = get_object_or_404(CicloInterarea, pk=ciclo_id)
        solicitud = ciclo_ia.nro_solicitudInterarea

        # Only the inter-area chief (inter_areaTematica) can sign
        try:
            if request.user.userprofile.rol not in PRIVILEGED_ROLES and \
               request.user.userprofile.area_tematica != solicitud.inter_areaTematica:
                return JsonResponse({'error': 'No tiene permisos para firmar este informe inter-area.'}, status=403)
        except AttributeError:
            return JsonResponse({'error': 'No tiene permisos.'}, status=403)

        sig_bytes = None
        profile = getattr(request.user, 'userprofile', None)
        if profile and profile.firma:
            sig_bytes = profile.firma.read()
        else:
            firma_b64 = request.data.get('firma_imagen', '')
            if firma_b64:
                _, data = firma_b64.split(',', 1)
                sig_bytes = b64lib.b64decode(data)

        if sig_bytes and ciclo_ia.adjunto_informeServicio_pdf:
            try:
                pdf_path = ciclo_ia.adjunto_informeServicio_pdf.path
                doc = fitz.open(pdf_path)

                for pg in doc:
                    pw, ph = pg.rect.width, pg.rect.height
                    sig_rect = fitz.Rect(15, ph - 150, 190, ph - 100)
                    pg.insert_image(sig_rect, stream=sig_bytes)

                page = doc[-1]
                pw, ph = page.rect.width, page.rect.height
                leyenda = (profile.leyenda.strip() if profile and profile.leyenda else '') or \
                          f"{request.user.first_name} {request.user.last_name}".strip() or \
                          request.user.username
                page.insert_textbox(
                    fitz.Rect(15, ph - 98, 190, ph - 72),
                    leyenda,
                    fontsize=7.5,
                    align=fitz.TEXT_ALIGN_CENTER,
                )

                buf = BytesIO()
                doc.save(buf)
                doc.close()
                buf.seek(0)

                original_name = os.path.basename(ciclo_ia.adjunto_informeServicio_pdf.name)
                nombre_base, ext = os.path.splitext(original_name)
                ciclo_ia.adjunto_firmado_area.save(
                    f"{nombre_base}_firmado_area{ext}",
                    ContentFile(buf.read()),
                    save=False,
                )
            except Exception:
                logger.exception("Error al insertar firma de área inter-area en PDF")

        ciclo_ia.firma_responsable_area = True
        ciclo_ia.save()
        _log(request, 'firma_responsable_area_ia',
             f'Firma del responsable inter-area registrada — cicloIA #{ciclo_ia.numero}, circuito #{solicitud.nro_circuito_id}',
             nro_circuito=solicitud.nro_circuito_id)
        return JsonResponse({'message': 'Firma del responsable inter-area confirmada correctamente.'})


class RechazarFirmaResponsableAreaCicloIA(APIView):
    permission_classes = [IsAuthenticated, IsAreaJefe]

    def put(self, request, ciclo_id):
        ciclo_ia = get_object_or_404(CicloInterarea, pk=ciclo_id)
        solicitud = ciclo_ia.nro_solicitudInterarea

        try:
            if request.user.userprofile.rol not in PRIVILEGED_ROLES and \
               request.user.userprofile.area_tematica != solicitud.inter_areaTematica:
                return JsonResponse({'error': 'No tiene permisos para rechazar este informe inter-area.'}, status=403)
        except AttributeError:
            return JsonResponse({'error': 'No tiene permisos.'}, status=403)

        destino = request.data.get('destino', 'st')
        nota = request.data.get('nota_rechazo', '')

        if ciclo_ia.adjunto_firmado_area:
            ciclo_ia.adjunto_firmado_area.delete(save=False)
            ciclo_ia.adjunto_firmado_area = None
        if ciclo_ia.adjunto_firmado_direccion:
            ciclo_ia.adjunto_firmado_direccion.delete(save=False)
            ciclo_ia.adjunto_firmado_direccion = None
        if ciclo_ia.adjunto_informeServicio_pdf:
            ciclo_ia.adjunto_informeServicio_pdf.delete(save=False)
            ciclo_ia.adjunto_informeServicio_pdf = None
        ciclo_ia.pdf_confirmado_admin = False
        ciclo_ia.firma_responsable_area = False
        ciclo_ia.firma_direccion = False
        ciclo_ia.revision_confirmada = False
        ciclo_ia.nota_rechazo_area = nota
        ciclo_ia.rechazo_area_destino = destino
        ciclo_ia.nota_rechazo_direccion = None
        ciclo_ia.rechazo_destino = None
        ciclo_ia.save()
        if nota:
            CorreccionIA.objects.create(
                ciclo_ia=ciclo_ia,
                tipo='area',
                destinatario=destino,
                descripcion=nota,
                autor=request.user,
            )
        _log(request, 'rechazar_firma_area_ia',
             f'Firma inter-area rechazada → {destino} — cicloIA #{ciclo_ia.numero}, circuito #{solicitud.nro_circuito_id}',
             nro_circuito=solicitud.nro_circuito_id)
        return JsonResponse({'message': 'Informe inter-area rechazado por responsable de área correctamente.'})


class ConfirmarFirmaDireccionCicloIA(APIView):
    permission_classes = [IsAuthenticated, IsDireccion]

    def put(self, request, ciclo_id):
        ciclo_ia = get_object_or_404(CicloInterarea, pk=ciclo_id)

        sig_bytes = None
        profile = getattr(request.user, 'userprofile', None)
        if profile and profile.firma:
            sig_bytes = profile.firma.read()
        else:
            firma_b64 = request.data.get('firma_imagen', '')
            if firma_b64:
                _, data = firma_b64.split(',', 1)
                sig_bytes = b64lib.b64decode(data)

        fuente = ciclo_ia.adjunto_firmado_area or ciclo_ia.adjunto_informeServicio_pdf
        if sig_bytes and fuente:
            try:
                doc = fitz.open(fuente.path)
                page = doc[-1]
                pw, ph = page.rect.width, page.rect.height

                sig_rect = fitz.Rect(pw - 190, ph - 150, pw - 15, ph - 100)
                page.insert_image(sig_rect, stream=sig_bytes)

                leyenda = (profile.leyenda.strip() if profile and profile.leyenda else '') or \
                          f"{request.user.first_name} {request.user.last_name}".strip() or \
                          request.user.username
                page.insert_textbox(
                    fitz.Rect(pw - 190, ph - 98, pw - 15, ph - 72),
                    leyenda,
                    fontsize=7.5,
                    align=fitz.TEXT_ALIGN_CENTER,
                )

                buf = BytesIO()
                doc.save(buf)
                doc.close()
                buf.seek(0)

                original_name = os.path.basename(fuente.name)
                nombre_base, _ = os.path.splitext(original_name)
                ciclo_ia.adjunto_firmado_direccion.save(
                    f"{nombre_base}_firmado_dir.pdf",
                    ContentFile(buf.read()),
                    save=False,
                )
            except Exception:
                logger.exception("Error al insertar firma de dirección inter-area en PDF")

        ciclo_ia.firma_direccion = True
        ciclo_ia.save()
        solicitud = ciclo_ia.nro_solicitudInterarea
        _log(request, 'firma_direccion_ia',
             f'Firma de Dirección inter-area registrada — cicloIA #{ciclo_ia.numero}, circuito #{solicitud.nro_circuito_id}',
             nro_circuito=solicitud.nro_circuito_id)
        return JsonResponse({'message': 'Firma de Dirección inter-area confirmada correctamente.'})


class RechazarFirmaDireccionCicloIA(APIView):
    permission_classes = [IsAuthenticated, IsDireccion]

    def put(self, request, ciclo_id):
        ciclo_ia = get_object_or_404(CicloInterarea, pk=ciclo_id)
        destino = request.data.get('destino', 'st')
        nota = request.data.get('nota_rechazo', '')

        if ciclo_ia.adjunto_firmado_area:
            ciclo_ia.adjunto_firmado_area.delete(save=False)
            ciclo_ia.adjunto_firmado_area = None
        if ciclo_ia.adjunto_firmado_direccion:
            ciclo_ia.adjunto_firmado_direccion.delete(save=False)
            ciclo_ia.adjunto_firmado_direccion = None
        if ciclo_ia.adjunto_informeServicio_pdf:
            ciclo_ia.adjunto_informeServicio_pdf.delete(save=False)
            ciclo_ia.adjunto_informeServicio_pdf = None
        ciclo_ia.pdf_confirmado_admin = False
        ciclo_ia.firma_direccion = False
        ciclo_ia.firma_responsable_area = False
        ciclo_ia.revision_confirmada = False

        if destino == 'area':
            if ciclo_ia.adjunto_informeServicio:
                ciclo_ia.adjunto_informeServicio.delete(save=False)
                ciclo_ia.adjunto_informeServicio = None
            if ciclo_ia.adjunto_informeArea:
                ciclo_ia.adjunto_informeArea.delete(save=False)
                ciclo_ia.adjunto_informeArea = None
            for registro in ciclo_ia.registros_ensayo.all():
                registro.archivo.delete(save=False)
                registro.delete()

        ciclo_ia.nota_rechazo_direccion = nota
        ciclo_ia.rechazo_destino = destino
        ciclo_ia.save()
        if nota:
            CorreccionIA.objects.create(
                ciclo_ia=ciclo_ia,
                tipo='direccion',
                destinatario=destino,
                descripcion=nota,
                autor=request.user,
            )
        solicitud = ciclo_ia.nro_solicitudInterarea
        _log(request, 'rechazar_firma_direccion_ia',
             f'Firma de Dirección inter-area rechazada → {destino} — cicloIA #{ciclo_ia.numero}, circuito #{solicitud.nro_circuito_id}',
             nro_circuito=solicitud.nro_circuito_id)
        return JsonResponse({'message': 'Informe inter-area rechazado por Dirección correctamente.'})


class ArchivarCircuito(APIView):
    permission_classes = [IsAuthenticated, IsAdministracionOrDireccion]

    def put(self, request, nro_circuito, *args, **kwargs):
        motivo = request.data.get('motivo_archivo', '')
        nota = request.data.get('nota_archivo', '')

        if not motivo:
            return Response({'error': 'Debe indicar el motivo de archivo.'}, status=status.HTTP_400_BAD_REQUEST)

        data_servicio = get_object_or_404(DataServicio, nro_circuito=nro_circuito)
        data_servicio.finalizado = True
        data_servicio.save()

        circuito = get_object_or_404(Circuito, nro_circuito=nro_circuito)
        circuito.finalizado = True
        circuito.motivo_archivo = motivo
        circuito.nota_archivo = nota if nota else None
        circuito.fecha_archivo = timezone.now()
        circuito.save()

        motivo_display = dict(MOTIVO_ARCHIVO_CHOICES).get(motivo, motivo)
        _log(request, 'archivar_circuito',
             f'Circuito #{nro_circuito} archivado — {motivo_display}',
             nro_circuito=int(nro_circuito))
        return JsonResponse({'message': 'Archivado correctamente.'})


class DesarchivarCircuito(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, nro_circuito):
        circuito = get_object_or_404(Circuito, nro_circuito=nro_circuito)
        if not circuito.finalizado:
            return Response({'error': 'El circuito no está archivado.'}, status=status.HTTP_400_BAD_REQUEST)

        data_servicio = get_object_or_404(DataServicio, nro_circuito=nro_circuito)
        data_servicio.finalizado = False
        data_servicio.save()

        circuito.finalizado = False
        circuito.motivo_archivo = ''
        circuito.nota_archivo = None
        circuito.fecha_archivo = None
        circuito.save()

        _log(request, 'desarchivar_circuito',
             f'Circuito #{nro_circuito} desarchivado y devuelto a En Curso',
             nro_circuito=int(nro_circuito))
        return JsonResponse({'message': 'Desarchivado correctamente.'})


class ObtenerArchivados(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        rol = get_user_rol(request)
        servicios = DataServicio.objects.filter(finalizado=True).select_related(
            'nro_presupuesto', 'nro_presupuesto__nro_solicitante', 'nro_circuito'
        )

        if rol not in PRIVILEGED_ROLES:
            user_area = get_user_area(request)
            presupuestos_area = Presupuesto.objects.filter(
                area_tematica=user_area
            ).values_list('nro_presupuesto', flat=True)
            interarea_circuitos = SolicitudInterarea.objects.filter(
                inter_areaTematica=user_area
            ).values_list('nro_circuito', flat=True)
            servicios = servicios.filter(
                Q(nro_presupuesto__in=presupuestos_area) |
                Q(nro_circuito__in=interarea_circuitos)
            )

        result = []
        for ds in servicios:
            presupuesto = ds.nro_presupuesto
            solicitante = presupuesto.nro_solicitante
            circuito = ds.nro_circuito

            legajo = Legajo.objects.filter(nro_circuito=circuito).first()

            ciclo_firmado = CicloInforme.objects.filter(
                nro_circuito=circuito, firma_direccion=True
            ).order_by('-numero').first()
            informe_firmado_url = None
            if ciclo_firmado and ciclo_firmado.adjunto_firmado_direccion:
                informe_firmado_url = request.build_absolute_uri(ciclo_firmado.adjunto_firmado_direccion.url)

            detalles = DetallePresupuesto.objects.filter(
                nro_presupuesto=presupuesto
            ).select_related('nro_servicio')

            servicios_list = [
                {
                    'nro_servicio': d.nro_servicio.nro_servicio,
                    'servicio': d.nro_servicio.servicio,
                    'norma': d.nro_servicio.norma,
                    'cant': d.cant,
                    'subtotal': str(d.subtotal),
                }
                for d in detalles
            ]

            motivo_key = circuito.motivo_archivo if circuito else None
            motivo_display = dict(MOTIVO_ARCHIVO_CHOICES).get(motivo_key, None) if motivo_key else None

            result.append({
                'nro_dataServicio': ds.nro_dataServicio,
                'nro_circuito': circuito.nro_circuito if circuito else None,
                'fecha_dataServicio': ds.fecha_dataServicio,
                'obra': ds.obra,
                'observaciones_servicio': ds.observaciones,
                'nro_presupuesto': presupuesto.nro_presupuesto,
                'area_tematica': presupuesto.area_tematica,
                'arancel_presupuesto': str(presupuesto.arancel_presupuesto),
                'descuento': presupuesto.descuento,
                'nombre_solicitante': solicitante.nombre_solicitante,
                'cuit_solicitante': solicitante.cuit,
                'nro_legajo': legajo.nro_legajo if legajo else None,
                'fecha_legajo': str(legajo.fecha_legajo) if legajo else None,
                'pago': legajo.pago if legajo else None,
                'informe_firmado': informe_firmado_url,
                'motivo_archivo': motivo_key,
                'motivo_archivo_display': motivo_display,
                'nota_archivo': circuito.nota_archivo if circuito else None,
                'fecha_archivo': circuito.fecha_archivo.strftime('%Y-%m-%d') if circuito and circuito.fecha_archivo else None,
                'servicios': servicios_list,
            })

        return JsonResponse(result, safe=False)


class ObtenerEventosAuditoria(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rol = get_user_rol(request)
        if rol not in PRIVILEGED_ROLES and rol != 'direccion':
            return Response({'error': 'Sin permisos.'}, status=status.HTTP_403_FORBIDDEN)
        eventos = EventoAuditoria.objects.select_related('usuario').order_by('-fecha')[:500]
        return Response(EventoAuditoriaSerializer(eventos, many=True).data)


class HistorialCircuito(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, nro_circuito):
        eventos = (
            EventoAuditoria.objects
            .filter(nro_circuito=nro_circuito)
            .select_related('usuario')
            .order_by('fecha')
        )
        return Response(EventoAuditoriaSerializer(eventos, many=True).data)


# Configuración ISO 17025
class ConfigFormularioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, tipo):
        try:
            config = ConfigFormulario.objects.prefetch_related('revisiones').get(tipo=tipo)
        except ConfigFormulario.DoesNotExist:
            return Response({'error': 'Formulario no encontrado'}, status=404)

        revisiones = [
            {
                'version': r.version,
                'fecha': r.fecha.strftime('%d/%m/%Y'),
                'descripcion': r.descripcion,
                'aprobado_por': r.aprobado_por,
            }
            for r in config.revisiones.all()
        ]
        # Fecha de la versión actual
        revision_actual = config.revisiones.filter(version=config.version_actual).first()
        fecha_version_actual = revision_actual.fecha.strftime('%d/%m/%Y') if revision_actual else ''

        return Response({
            'tipo': config.tipo,
            'nombre': config.nombre,
            'codigo': config.codigo,
            'version_actual': config.version_actual,
            'fecha_version_actual': fecha_version_actual,
            'revisiones': revisiones,
        })
    