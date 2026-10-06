from django.urls import path
from .views import PresupuestoListView, PresupuestoDetailView, obtener_todos_los_presupuestos, buscar_solicitantes, seleccionar_solicitante, buscar_servicios, seleccionar_servicio, presupuestos_enEspera, actualizar_estado_presupuesto, presupuestos_cancelados, presupuestos_aceptados, obtener_presupuesto, generar_pdf_presupuesto

urlpatterns = [
    path('', PresupuestoListView.as_view(), name='presupuestos-list'),
    path('<int:pk>/', PresupuestoDetailView.as_view(), name='aranceles-detail'),
    path('todos/', obtener_todos_los_presupuestos, name='presupuestos-todos'),
    path('buscar_solicitantes/', buscar_solicitantes, name='buscar-solicitantes'),
    path('seleccionar_solicitante/<int:nro_solicitante>/', seleccionar_solicitante, name='selecciono-solicitante'),
    path('buscar_servicios/', buscar_servicios, name='buscar-servicios'),
    path('seleccionar_servicio/<int:nro_servicio>/', seleccionar_servicio, name='selecciono-servicio'),
    path('en_espera/', presupuestos_enEspera, name='presupuestos_enEspera'),
    path('aceptados/', presupuestos_aceptados, name='presupuestos_aceptados'),
    path('cancelados/', presupuestos_cancelados, name='presupuestos_cancelados'),
    path('actualizar_estado/<int:nro_presupuesto>/', actualizar_estado_presupuesto, name='actualizar_estado_presupuesto'),
    # path('obtener_modulo/', obtener_modulo, name='obtener-modulo'),
    path('obtener_presupuesto/<int:nro_presupuesto>/', obtener_presupuesto, name='obtener-presupuesto'),
    path('generar_pdf_presupuesto/<int:nro_presupuesto>/', generar_pdf_presupuesto, name='generar-pdf-presupuesto'),
]
