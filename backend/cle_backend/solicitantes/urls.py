from django.urls import path
from .views import SolicitanteListView, SolicitanteDetailView, obtener_todos_los_solicitantes

urlpatterns = [
    path('solicitantes/', SolicitanteListView.as_view(), name='solicitantes-list'),
    path('solicitantes/<int:pk>/', SolicitanteDetailView.as_view(), name='solicitantes-detail'),
    path('solicitantes/todos/', obtener_todos_los_solicitantes, name='solicitantes-todos'),
]
