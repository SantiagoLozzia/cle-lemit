from django.urls import path
from .views import ServicioListView, ServicioDetailView, obtener_todos_los_aranceles

urlpatterns = [
    path('aranceles/', ServicioListView.as_view(), name='aranceles-list'),
    path('aranceles/<int:pk>/', ServicioDetailView.as_view(), name='aranceles-detail'),
    path('aranceles/todos/', obtener_todos_los_aranceles, name='aranceles-todos'),
]
