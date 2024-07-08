from django.shortcuts import render
from .serializers import *
from database.models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views import View 
from django.utils import timezone
from django.middleware.csrf import get_token

# Cargar la Tabla
class ObtenerTodoEnCurso(APIView):
    def get(self, request, format=None):
        # Obtener todos los DataServicio donde DataServicio.finalizado = False
        servicios_en_curso = DataServicio.objects.filter(finalizado=False)

        # Obtener el numero de presupuesto de los DataServicio
        numeros_presupuesto = servicios_en_curso.values_list('nro_presupuesto', flat=True)

        # Obtener el área temática de cada presupuesto y el nro_solicitante
        presupuestos = Presupuesto.objects.filter(nro_presupuesto__in=numeros_presupuesto).select_related('nro_solicitante')
        presupuesto_map = {presupuesto.nro_presupuesto: (presupuesto.area_tematica, presupuesto.nro_solicitante.nombre_solicitante) for presupuesto in presupuestos}

        # Serializar los datos de los DataServicio
        servicios_en_curso_serializer = DataServicioSerializer(servicios_en_curso, many=True)

        # Agregar los campos 'area_tematica' y 'nombre_solicitante' a los datos de DataServicio
        for data_servicio in servicios_en_curso_serializer.data:
            nro_presupuesto = data_servicio['nro_presupuesto']
            area_tematica, nombre_solicitante = presupuesto_map.get(nro_presupuesto, ('', ''))
            data_servicio['area_tematica'] = area_tematica
            data_servicio['nombre_solicitante'] = nombre_solicitante

        # Obtener el numero de circuito de los DataServicio
        numeros_circuito = servicios_en_curso.values_list('nro_circuito', flat=True)
        # circuitos = Circuito.objects.filter(nro_circuito__in=servicios_en_curso.values_list('nro_circuito', flat=True))

        # Obtener los datos de los otros modelos
        legajos = Legajo.objects.filter(nro_circuito__in=numeros_circuito)
        recepciones = Recepcion.objects.filter(nro_circuito__in=numeros_circuito)
        ordenes_servicio = OrdenServicio.objects.filter(nro_circuito__in=numeros_circuito)
        informes_area = InformeArea.objects.filter(nro_circuito__in=numeros_circuito)
        informes_servicio = InformeServicio.objects.filter(nro_circuito__in=numeros_circuito)
        solicitudes_inter_area = SolicitudInterarea.objects.filter(nro_circuito__in=numeros_circuito)
        informes_inter_area = InformeInterarea.objects.filter(nro_circuito__in=numeros_circuito)

        # Serializar los datos
        legajos_serializer = LegajoEnCursoSerializer(legajos, many=True)
        recepciones_serializer = RecepcionEnCursoSerializer(recepciones, many=True)
        ordenes_servicio_serializer = OrdenServicioEnCursoSerializer(ordenes_servicio, many=True)
        informes_area_serializer = InformeAreaEnCursoSerializer(informes_area, many=True)
        informes_servicio_serializer = InformeServicioEnCursoSerializer(informes_servicio, many=True)
        solicitudes_inter_area_serializer = SolicitudInterAreaEnCursoSerializer(solicitudes_inter_area, many=True)
        informes_inter_area_serializer = InformeInterAreaEnCursoSerializer(informes_inter_area, many=True)

        # Construir la respuesta
        response_data = {
            'solicitudes': servicios_en_curso_serializer.data,
            'legajos': legajos_serializer.data,
            'recepciones': recepciones_serializer.data,
            'ordenes_servicio': ordenes_servicio_serializer.data,
            'informes_area': informes_area_serializer.data,
            'informes_servicio': informes_servicio_serializer.data,
            'solicitudes_inter_area': solicitudes_inter_area_serializer.data,
            'informes_inter_area': informes_inter_area_serializer.data
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

def presupuesto_seleccionado(request, nro_presupuesto):
    try:
        presupuesto = Presupuesto.objects.select_related('nro_solicitante').get(nro_presupuesto=nro_presupuesto)
        # Obtiene el nombre del solicitante asociado al presupuesto
        nombre_solicitante = presupuesto.nro_solicitante.nombre_solicitante
        
        # Construye el diccionario de datos a devolver
        data = {
            'nro_presupuesto': presupuesto.nro_presupuesto,
            'nombre_solicitante': nombre_solicitante,
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
                presupuesto.estado_presupuesto = 'aceptado'  # Cambiar aquí al estado deseado
                presupuesto.save()
            except Presupuesto.DoesNotExist:
                pass  # Manejar el caso donde no se encuentra el presupuesto

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
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
class GuardarAdjuntoSolicitud(APIView):
    def post(self, request):
        nro_dataServicio = request.data.get('nroDataServicio')
        data_servicio = DataServicio.objects.get(nro_dataServicio=nro_dataServicio)
        adjunto = request.FILES.get('archivo')
        data_servicio.adjunto_solicitudServicio = adjunto
        data_servicio.completo = True
        data_servicio.save()
        serializer = GuardarAdjuntoSolicitudDataServicioSerializer(data_servicio)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# Legajo
def obtener_rangoLab(request, nro_circuito):
    # Obtener la instancia de DataServicio correspondiente al nro_circuito
    dataservicio = get_object_or_404(DataServicio, nro_circuito=nro_circuito)

    # Obtener el último número usando la clase Singleton
    singleton = UltimoNumeroSingleton()
    ultimo_numero = singleton.ultimo_numero

    # Calcular el rango de laboratorios
    inicio_rango = ultimo_numero + 1
    cantidad_numeros = dataservicio.cant_numLabs
    final_rango = inicio_rango + cantidad_numeros - 1
    rangLab = f"{inicio_rango}-{final_rango}"

    # Devolver la respuesta como JSON incluyendo el rangoLab y el último número
    response_data = {
        'rangoLab': rangLab,
        'ultimo_numero': final_rango
    }

    return JsonResponse(response_data)

class CrearLegajo(APIView):
    def post(self, request):
        # Obtener el número de circuito del request
        nro_circuito = request.data.get('nro_circuito')
        
        try:
            # Verificar si el circuito existe
            circuito_instance = Circuito.objects.get(nro_circuito=nro_circuito)

            # Crear los datos del legajo con la instancia de circuito
            legajo_data = request.data.copy()
            legajo_data['nro_circuito'] = circuito_instance.pk  # lave primaria (ID) del circuito

            # Serializar los datos del legajo
            serializer = LegajoEnCursoSerializer(data=legajo_data)
            if serializer.is_valid():
                # Guardar el legajo
                serializer.save()
                
                # Actualizar el último número en la clase Singleton
                singleton = UltimoNumeroSingleton()
                singleton.ultimo_numero = request.data.get('nuevo_ultimo_numero')

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
            'nombre_solicitante': nombre_solicitante
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
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

class GuardarAdjuntoFactura(APIView):
    def post(self, request):
        try:
            nro_legajo = request.data.get('nroLegajo')
            adjunto = request.FILES.get('archivo')
            nro_circuito = request.data.get('nroCircuito')

            # Buscar la recepcion existente por nro_circuito
            recepcion_existente = Recepcion.objects.filter(nro_circuito_id=nro_circuito).first()

            if not recepcion_existente:
                # Si no existe, crear una nueva instancia de Recepcion
                circuito = get_object_or_404(Circuito, pk=nro_circuito)
                nueva_recepcion = Recepcion.objects.create(nro_circuito=circuito)

            # Guardar el adjunto en Legajo y marcar como completo
            legajo = get_object_or_404(Legajo, nro_legajo=nro_legajo)
            legajo.adjunto_factura = adjunto
            legajo.completo = True
            legajo.save()

            # Serializar y devolver la respuesta
            serializer = GuardarAdjuntoFacturaSerializer(legajo)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            nueva_instancia = OrdenServicio.objects.create(nro_circuito=circuito, fecha_ordenServicio=fecha_actual, observaciones='', completo=True)
            return JsonResponse({'mensaje': 'Orden de servicio creada exitosamente', 'nro_circuito': nro_circuito}, status=201)
        except Circuito.DoesNotExist:
            return JsonResponse({'mensaje': 'Circuito no encontrado', 'nro_circuito': nro_circuito}, status=404)
        except Exception as e:
            print(f"Error: {e}")  # Depuración
            return JsonResponse({'mensaje': 'Error al crear la orden de servicio', 'error': str(e)}, status=400)

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

        # Obtener los detalles de Presupuesto y serializarlos
        detalle_presupuestos = DetallePresupuesto.objects.select_related('nro_servicio') \
                                                         .filter(nro_presupuesto=nro_presupuesto)
        serializer = DetallePresupuestoSerializer(detalle_presupuestos, many=True)
        servicio_solicitado = serializer.data

        # Crear el diccionario de respuesta con los datos obtenidos
        response_data = {
            'nro_ordenServicio': nro_ordenServicio,
            'fecha_ordenServicio': fecha_ordenServicio,
            'area_tematica': area_tematica,
            'nro_legajo': nro_legajo,
            'rangos_laboratorios': rangos_laboratorios,
            'plazo_estimado': plazo_estimado,
            'nombre_solicitante': nombre_solicitante,
            'servicio_solicitado': servicio_solicitado,
            'muestras': muestras,
            'observaciones': observaciones,
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
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Informe de Area    
class GuardarAdjuntoInformeArea(APIView):
    def post(self, request):
        try:
            # Obtener el archivo y el nro_circuito del request
            adjunto = request.FILES.get('archivo')
            nro_circuito = request.data.get('nroCircuito')

            if not adjunto or not nro_circuito:
                return Response({'error': 'Archivo y nro_circuito son requeridos'}, status=status.HTTP_400_BAD_REQUEST)

            # Crear una instancia de InformeArea
            informe_area = InformeArea(
                fecha_informeArea=timezone.now().date(),
                adjunto_informeArea=adjunto,
                completo=False,
                estado_informeArea='sin_informe',  # Usar el valor correcto de tu elección
                nro_circuito_id=nro_circuito  # Asignar el nro_circuito directamente
            )
            informe_area.save()

            # Serializar los datos de la nueva instancia
            serializer = InformeAreaEnCursoSerializer(informe_area)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    