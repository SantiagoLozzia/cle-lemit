from django.urls import path
from .views import *
urlpatterns = [
    path('encurso/buscar_presupuestos/', NrosPresupuestoEnEspera.as_view(), name='presupuestos-list'),
    path('encurso/presupuesto_seleccionado/<int:nro_presupuesto>/', presupuesto_seleccionado, name='presupuesto-seleccionado'),
    # Solicitud de Servicio
    path('encurso/crear_dataServicio/', CrearDataServicioView.as_view(), name='crear-dataservicio'),
    path('encurso/obtener_todoencurso/', ObtenerTodoEnCurso.as_view(), name='obtener-todosencurso'),
    path('encurso/obtener_dataservicio/<int:nro_dataServicio>/', obtener_dataServicio, name= 'obtener-dataServicio'),
    path('encurso/guardar_adjuntosolicitudservicio/', GuardarAdjuntoSolicitud.as_view(), name='guardar-adjuntosolicitud'),
    # Legajo
    path('encurso/obtener_legajo/<int:nro_circuito>/', obtener_legajo, name= 'obtener-legajo'),
    path('encurso/obtener_rangoLab/<int:nro_circuito>/', obtener_rangoLab, name= 'obtener-rangoLab'),
    path('encurso/crear_legajo/', CrearLegajo.as_view(), name='crear-legajo'),
    path('encurso/guardar_adjuntofactura/', GuardarAdjuntoFactura.as_view(), name='guardar-adjuntofactura'),
    path('encurso/guardar_pago_legajo/<int:nro_circuito>/', GuardarPagoLegajo.as_view(), name='guardar-pagoLegajo'),
    path('encurso/cambiar_plazo_pago/<int:nro_circuito>/', CambiarPlazoPago.as_view(), name='cambiar-plazoPago'),
    # Recepcion
    path('encurso/cambiar_remito/<int:nro_circuito>/', CambiarRemito.as_view(), name='cambiar-remito'),
    path('encurso/guardar_estado_recepcion/<int:nro_circuito>/', GuardarEstadoRecepcion.as_view(), name='guardar-estadoRecepcion'),
    path('encurso/cambiar_plazo_muestras/<int:nro_circuito>/', CambiarPlazoMuestras.as_view(), name='cambiar-plazoMuestras'),
    # Orden de Servicio
    path('encurso/crear_ordenservicio/<int:nro_circuito>/', CrearOrdenServicio.as_view(), name='crear-ordenservicio'),
    path('encurso/obtener_orden_servicio/<int:nro_circuito>/', obtener_ordenServicio, name= 'obtener-ordenServicio'),
    # Informe Area
    path('encurso/guardar_adjunto_informearea/', GuardarAdjuntoInformeArea.as_view(), name='guardar-adjuntoinformearea'),
]