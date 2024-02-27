from django.urls import path
from .views import NrosPresupuestoEnEspera, presupuesto_seleccionado, GuardarDataServicioView, ObtenerServiciosEnCurso, GuardarAdjuntoSolicitud

urlpatterns = [
    path('encurso/buscar_presupuestos/', NrosPresupuestoEnEspera.as_view(), name='presupuestos-list'),
    path('encurso/presupuesto_seleccionado/<int:nro_presupuesto>/', presupuesto_seleccionado, name='presupuesto-seleccionado'),
    path('encurso/guardar_dataServicio/', GuardarDataServicioView.as_view(), name='guardar-dataservicio'),
    path('encurso/obtener_serviciosencurso/', ObtenerServiciosEnCurso.as_view(), name='obtener-serviciosencurso'),
    path('encurso/guardar_adjuntosolicitudservicio/', GuardarAdjuntoSolicitud.as_view(), name='guardar-adjuntosolicitud'),
]