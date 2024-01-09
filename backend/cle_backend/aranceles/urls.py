from django.urls import path
from .views import ServicioListView, ServicioDetailView

urlpatterns = [
    path('aranceles/', ServicioListView.as_view(), name='aranceles-list'),
    path('aranceles/<int:pk>/', ServicioDetailView.as_view(), name='aranceles-detail'),
]
