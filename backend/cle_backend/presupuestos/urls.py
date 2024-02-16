from django.urls import path
from .views import PresupuestoListView, PresupuestoDetailView, obtener_todos_los_presupuestos, buscar_solicitantes

urlpatterns = [
    path('presupuestos/', PresupuestoListView.as_view(), name='presupuestos-list'),
    path('presupuestos/<int:pk>/', PresupuestoDetailView.as_view(), name='aranceles-detail'),
    path('presupuestos/todos/', obtener_todos_los_presupuestos, name='presupuestos-todos'),
    path('presupuestos/buscar_solicitantes/', buscar_solicitantes, name='buscar-solicitantes'),
]
