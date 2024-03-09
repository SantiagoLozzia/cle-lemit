from django.urls import path
from .views import NrosPresupuestoEnEspera, presupuesto_seleccionado, GuardarDataServicioView, ObtenerTodoEnCurso, obtener_dataServicio, GuardarAdjuntoSolicitud, obtener_legajo, obtener_rangoLab, GuardarLegajo, crear_ordenServicio, obtener_ordenServicio

urlpatterns = [
    path('encurso/buscar_presupuestos/', NrosPresupuestoEnEspera.as_view(), name='presupuestos-list'),
    path('encurso/presupuesto_seleccionado/<int:nro_presupuesto>/', presupuesto_seleccionado, name='presupuesto-seleccionado'),
    path('encurso/guardar_dataServicio/', GuardarDataServicioView.as_view(), name='guardar-dataservicio'),
    path('encurso/obtener_todoencurso/', ObtenerTodoEnCurso.as_view(), name='obtener-todosencurso'),
    path('encurso/obtener_dataservicio/<int:nro_dataServicio>/', obtener_dataServicio, name= 'obtener-dataServicio'),
    path('encurso/guardar_adjuntosolicitudservicio/', GuardarAdjuntoSolicitud.as_view(), name='guardar-adjuntosolicitud'),
    path('encurso/obtener_legajo/<int:nro_circuito>/', obtener_legajo, name= 'obtener-legajo'),
    path('encurso/obtener_rangoLab/<int:nro_circuito>/', obtener_rangoLab, name= 'obtener-rangoLab'),
    path('encurso/guardar_legajo/', GuardarLegajo.as_view(), name='guardar-legajo'),
    path('encurso/crear_ordenservicio/<int:nro_circuito>/', crear_ordenServicio, name='crear-ordenservicio'),
    path('encurso/obtener_orden_servicio/<int:nro_circuito>/', obtener_ordenServicio, name= 'obtener-ordenServicio')
]