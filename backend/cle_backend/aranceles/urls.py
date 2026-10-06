from django.urls import path
from .views import ServicioListView, ServicioDetailView, obtener_todos_los_aranceles, actualizar_modulo, obtener_modulo

urlpatterns = [
    path('', ServicioListView.as_view(), name='aranceles-list'),
    path('<int:pk>/', ServicioDetailView.as_view(), name='aranceles-detail'),
    path('todos/', obtener_todos_los_aranceles, name='aranceles-todos'),
    path('obtener_modulo/', obtener_modulo, name='obtener-modulo'),
    path('actualizar_modulo/', actualizar_modulo, name='actualizar-modulo'),
]
