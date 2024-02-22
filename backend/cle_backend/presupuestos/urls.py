from django.urls import path
from .views import PresupuestoListView, PresupuestoDetailView, obtener_todos_los_presupuestos, buscar_solicitantes, seleccionar_solicitante, buscar_servicios, seleccionar_servicio, presupuestos_enEspera, actualizar_estado_presupuesto, presupuestos_cancelados

urlpatterns = [
    path('presupuestos/', PresupuestoListView.as_view(), name='presupuestos-list'),
    path('presupuestos/<int:pk>/', PresupuestoDetailView.as_view(), name='aranceles-detail'),
    path('presupuestos/todos/', obtener_todos_los_presupuestos, name='presupuestos-todos'),
    path('presupuestos/buscar_solicitantes/', buscar_solicitantes, name='buscar-solicitantes'),
    path('presupuestos/seleccionar_solicitante/<int:nro_solicitante>/', seleccionar_solicitante, name='selecciono-solicitante'),
    path('presupuestos/buscar_servicios/', buscar_servicios, name='buscar-servicios'),
    path('presupuestos/seleccionar_servicio/<int:nro_servicio>/', seleccionar_servicio, name='selecciono-servicio'),
    path('presupuestos/en_espera/', presupuestos_enEspera, name='presupuestos_enEspera'),
    path('presupuestos/actualizar_estado/<int:nro_presupuesto>/', actualizar_estado_presupuesto, name='actualizar_estado_presupuesto'),
    path('presupuestos/cancelados/', presupuestos_cancelados, name='presupuestos_cancelados'),
]
