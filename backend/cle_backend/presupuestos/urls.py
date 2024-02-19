from django.urls import path
from .views import PresupuestoListView, PresupuestoDetailView, obtener_todos_los_presupuestos, buscar_solicitantes, seleccionar_solicitante, buscar_servicios, seleccionar_servicio

urlpatterns = [
    path('presupuestos/', PresupuestoListView.as_view(), name='presupuestos-list'),
    path('presupuestos/<int:pk>/', PresupuestoDetailView.as_view(), name='aranceles-detail'),
    path('presupuestos/todos/', obtener_todos_los_presupuestos, name='presupuestos-todos'),
    path('presupuestos/buscar_solicitantes/', buscar_solicitantes, name='buscar-solicitantes'),
    path('presupuestos/seleccionar_solicitante/<int:nro_solicitante>/', seleccionar_solicitante, name='selecciono-solicitante'),
    path('presupuestos/buscar_servicios/', buscar_servicios, name='buscar-servicios'),
    path('presupuestos/seleccionar_servicio/<int:nro_servicio/', seleccionar_servicio, name='selecciono-servicio'),
]
