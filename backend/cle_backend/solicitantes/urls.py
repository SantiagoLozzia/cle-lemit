from django.urls import path
from .views import SolicitanteListView, SolicitanteDetailView, obtener_todos_los_solicitantes

urlpatterns = [
    path('', SolicitanteListView.as_view(), name='solicitantes-list'),
    path('<int:pk>/', SolicitanteDetailView.as_view(), name='solicitantes-detail'),
    path('todos/', obtener_todos_los_solicitantes, name='solicitantes-todos'),
]
