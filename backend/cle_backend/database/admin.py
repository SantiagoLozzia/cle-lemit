from django.contrib import admin
from .models import EventoAuditoria


@admin.register(EventoAuditoria)
class EventoAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'usuario', 'accion', 'descripcion', 'nro_circuito')
    list_filter = ('accion', 'usuario')
    search_fields = ('descripcion', 'usuario__username', 'accion')
    readonly_fields = ('fecha', 'usuario', 'accion', 'descripcion', 'nro_circuito')
    ordering = ('-fecha',)
