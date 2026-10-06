from django.urls import path
from .views import *
urlpatterns = [
    path('buscar_presupuestos/', NrosPresupuestoEnEspera.as_view(), name='presupuestos-list'),
    path('presupuesto_seleccionado/<int:nro_presupuesto>/', presupuesto_seleccionado, name='presupuesto-seleccionado'),
    # Solicitud de Servicio
    path('crear_dataServicio/', CrearDataServicioView.as_view(), name='crear-dataservicio'),
    path('obtener_todoencurso/', ObtenerTodoEnCurso.as_view(), name='obtener-todosencurso'),
    path('obtener_dataservicio/<int:nro_dataServicio>/', obtener_dataServicio, name= 'obtener-dataServicio'),
    path('guardar_adjuntosolicitudservicio/', GuardarAdjuntoSolicitud.as_view(), name='guardar-adjuntosolicitud'),
    # Legajo
    path('obtener_legajo/<int:nro_circuito>/', obtener_legajo, name= 'obtener-legajo'),
    path('obtener_rangoLab/<int:nro_circuito>/', obtener_rangoLab, name= 'obtener-rangoLab'),
    path('crear_legajo/', CrearLegajo.as_view(), name='crear-legajo'),
    path('guardar_adjuntofactura/', GuardarAdjuntoFactura.as_view(), name='guardar-adjuntofactura'),
    path('guardar_pago_legajo/<int:nro_circuito>/', GuardarPagoLegajo.as_view(), name='guardar-pagoLegajo'),
    path('cambiar_plazo_pago/<int:nro_circuito>/', CambiarPlazoPago.as_view(), name='cambiar-plazoPago'),
    path('generar_pdf_legajo/<int:nro_circuito>/', generar_pdf_legajo, name='generar-pdf-legajo'),
    # Recepcion
    path('cambiar_remito/<int:nro_circuito>/', CambiarRemito.as_view(), name='cambiar-remito'),
    path('guardar_estado_recepcion/<int:nro_circuito>/', GuardarEstadoRecepcion.as_view(), name='guardar-estadoRecepcion'),
    path('cambiar_plazo_muestras/<int:nro_circuito>/', CambiarPlazoMuestras.as_view(), name='cambiar-plazoMuestras'),
    # Orden de Servicio
    path('crear_ordenservicio/<int:nro_circuito>/', CrearOrdenServicio.as_view(), name='crear-ordenservicio'),
    path('obtener_orden_servicio/<int:nro_circuito>/', obtener_ordenServicio, name= 'obtener-ordenServicio'),
    path('cambiar_plazo_estimado/<int:nro_circuito>/', CambiarPlazoEstimado.as_view(), name= 'cambiar-plazo-estimado'),
    # Informe Area
    path('guardar_adjunto_informearea/', GuardarAdjuntoInformeArea.as_view(), name='guardar-adjunto-informearea'),
    path('guardar_registros_ensayo/', GuardarRegistrosEnsayo.as_view(), name='guardar-registros-ensayo'),
    # Inter Area
    path('obtener_servicios/<int:nro_circuito>/', obtener_servicios, name='obtener-servicios'),
    path('crear_solicitud_interarea/', CrearSolicitudInterarea.as_view(), name='crear-solicitud-interarea'),
    path('obtener_solicitud_interarea/<int:nro_circuito>/', obtener_solicitudInterarea, name='obtener-solicitud-interarea'),
    path('guardar_adjuntoinformeinterarea/', GuardarAdjuntoInformeInterarea.as_view(), name='guardar-adjuntoinformeinterarea'),
    path('guardar_adjuntoinformeservicio/', GuardarAdjuntoInformeServicio.as_view(), name='guardar-adjuntoinformeservicio'),
    # Administracion
    path('obtener_correcciones/<int:nro_circuito>/', obtener_correcciones, name='obtener-correcciones'),
    path('corregir_informe_servicio/<int:nro_circuito>/', CorregirInformeServicio.as_view(), name= 'corregir-informr-servicio'),
    # Revision
    path('confirmar_revision/<int:nro_circuito>/', ConfirmarRevision.as_view(), name='confirmar_revision'),
    # Firma Responsable Area
    path('confirmar_firma_responsable_area/<int:nro_circuito>/', ConfirmarFirmaResponsableArea.as_view(), name='confirmar-firma-responsable-area'),
    path('advertir_correcciones/<int:nro_circuito>/', AdvertirCorrecciones.as_view(), name='advertir-correcciones'),
    # Firma Dirección
    path('guardar_adjuntoinformeserviciofirmado/', GuardarAdjuntoInformeServicioFirmado.as_view(), name='guardar-adjuntoinformeservicio-firmado'),
    path('confirmar_firma_direccion/<int:nro_circuito>/', ConfirmarFirmaDireccion.as_view(), name='confirmar-firma-direccion'),
    # Archivar
    path('archivar_circuito/<int:nro_circuito>/', ArchivarCircuito.as_view(), name='archivar-circuito'),



    
]