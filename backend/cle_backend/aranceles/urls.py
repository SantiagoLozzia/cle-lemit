from django.urls import path
from .views import ServicioListView, ServicioDetailView, obtener_todos_los_aranceles, actualizar_modulo, obtener_modulo

urlpatterns = [
    path('aranceles/', ServicioListView.as_view(), name='aranceles-list'),
    path('aranceles/<int:pk>/', ServicioDetailView.as_view(), name='aranceles-detail'),
    path('aranceles/todos/', obtener_todos_los_aranceles, name='aranceles-todos'),
    path('aranceles/obtener_modulo/', obtener_modulo, name='obtener-modulo'),
    path('aranceles/actualizar_modulo/', actualizar_modulo, name='actualizar-modulo'),
]
