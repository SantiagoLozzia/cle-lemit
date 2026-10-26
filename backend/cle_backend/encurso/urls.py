from django.urls import path
from .views import *
urlpatterns = [
    path('archivados/', ObtenerArchivados.as_view(), name='obtener-archivados'),
    path('buscar_presupuestos/', NrosPresupuestoEnEspera.as_view(), name='presupuestos-list'),
    path('presupuesto_seleccionado/<int:nro_presupuesto>/', presupuesto_seleccionado, name='presupuesto-seleccionado'),
    # Solicitud de Servicio
    path('crear_dataServicio/', CrearDataServicioView.as_view(), name='crear-dataservicio'),
    path('obtener_todoencurso/', ObtenerTodoEnCurso.as_view(), name='obtener-todosencurso'),
    path('obtener_dataservicio/<int:nro_dataServicio>/', obtener_dataServicio, name='obtener-dataServicio'),
    path('guardar_adjuntosolicitudservicio/', GuardarAdjuntoSolicitud.as_view(), name='guardar-adjuntosolicitud'),
    # Legajo
    path('obtener_legajo/<int:nro_circuito>/', obtener_legajo, name='obtener-legajo'),
    path('obtener_rangoLab/<int:nro_circuito>/', obtener_rangoLab, name='obtener-rangoLab'),
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
    path('preview_ordenservicio/<int:nro_circuito>/', preview_ordenservicio, name='preview-ordenservicio'),
    path('obtener_orden_servicio/<int:nro_circuito>/', obtener_ordenServicio, name='obtener-ordenServicio'),
    path('cambiar_plazo_estimado/<int:nro_circuito>/', CambiarPlazoEstimado.as_view(), name='cambiar-plazo-estimado'),
    # Ciclos de Informe
    path('crear_ciclo/<int:nro_circuito>/', CrearCiclo.as_view(), name='crear-ciclo'),
    path('subir_informe_area_ciclo/<int:ciclo_id>/', SubirInformeAreaCiclo.as_view(), name='subir-informe-area-ciclo'),
    path('subir_registro_ensayo_ciclo/<int:ciclo_id>/', SubirRegistroEnsayoCiclo.as_view(), name='subir-registro-ensayo-ciclo'),
    path('registro_ensayo_ciclo/<int:pk>/', EliminarRegistroEnsayoCiclo.as_view(), name='eliminar-registro-ensayo-ciclo'),
    path('informe_area_ciclo/<int:ciclo_id>/', EliminarInformeAreaCiclo.as_view(), name='eliminar-informe-area-ciclo'),
    path('cambiar_tipo_ciclo/<int:ciclo_id>/', CambiarTipoCiclo.as_view(), name='cambiar-tipo-ciclo'),
    path('subir_informe_servicio_ciclo/<int:ciclo_id>/', SubirInformeServicioCiclo.as_view(), name='subir-informe-servicio-ciclo'),
    path('obtener_correcciones_ciclo/<int:ciclo_id>/', obtener_correcciones_ciclo, name='obtener-correcciones-ciclo'),
    path('advertir_correcciones_ciclo/<int:ciclo_id>/', AdvertirCorreccionesCiclo.as_view(), name='advertir-correcciones-ciclo'),
    path('corregir_ciclo/<int:ciclo_id>/', CorregirCiclo.as_view(), name='corregir-ciclo'),
    path('confirmar_revision_ciclo/<int:ciclo_id>/', ConfirmarRevisionCiclo.as_view(), name='confirmar-revision-ciclo'),
    path('subir_informe_st_corregido/<int:ciclo_id>/', SubirInformeSTCorregido.as_view(), name='subir-informe-st-corregido'),
    path('registrar_correccion_st/<int:ciclo_id>/', RegistrarCorreccionST.as_view(), name='registrar-correccion-st'),
    path('confirmar_firma_responsable_area_ciclo/<int:ciclo_id>/', ConfirmarFirmaResponsableAreaCiclo.as_view(), name='confirmar-firma-responsable-area-ciclo'),
    path('confirmar_firma_direccion_ciclo/<int:ciclo_id>/', ConfirmarFirmaDireccionCiclo.as_view(), name='confirmar-firma-direccion-ciclo'),
    # Editar Data Servicio
    path('editar_dataservicio/<int:nro_dataServicio>/', EditarDataServicio.as_view(), name='editar-dataservicio'),
    path('aprobar_labs_adicionales/<int:nro_circuito>/', AprobarLabsAdicionales.as_view(), name='aprobar-labs-adicionales'),
    # Eliminar adjuntos por ID
    path('adjunto_solicitud/<int:pk>/', EliminarAdjuntoSolicitud.as_view(), name='eliminar-adjunto-solicitud'),
    path('adjunto_factura/<int:pk>/', EliminarAdjuntoFactura.as_view(), name='eliminar-adjunto-factura'),
    path('informe_interarea/<int:pk>/', EliminarInformeInterarea.as_view(), name='eliminar-informe-interarea'),
    # Inter Area
    path('obtener_servicios/<int:nro_circuito>/', obtener_servicios, name='obtener-servicios'),
    path('crear_solicitud_interarea/', CrearSolicitudInterarea.as_view(), name='crear-solicitud-interarea'),
    path('obtener_solicitud_interarea/<int:nro_circuito>/', obtener_solicitudInterarea, name='obtener-solicitud-interarea'),
    path('guardar_adjuntoinformeinterarea/', GuardarAdjuntoInformeInterarea.as_view(), name='guardar-adjuntoinformeinterarea'),
    # Archivar
    path('archivar_circuito/<int:nro_circuito>/', ArchivarCircuito.as_view(), name='archivar-circuito'),
]
