from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from database.models import *

class Command(BaseCommand):
    help = 'Create the group area_jefe and assign permissions'

    def handle(self, *args, **options):
        # Crear Grupo 'area_jefe'
        area_jefe_group, created = Group.objects.get_or_create(name='area_jefe')

        # Asignar permisos al grupo 'area_jefe'
        models_permissions = {
            Solicitante: ['view_solicitante'],
            Presupuesto: ['view_presupuesto'],
            Servicio: ['view_servicio'],
            DetallePresupuesto: ['view_detallepresupuesto'],
            DataServicio: ['view_dataservicio'],
            Legajo: ['view_legajo'],
            Recepcion: ['view_recepcion'],
            OrdenServicio: ['view_ordenservicio'],
            InformeArea: ['view_informearea','change_informearea', 'add_informearea', 'delete_informearea'],
            InformeServicio: ['view_informeservicio', 'change_informeservicio'],
            SolicitudInterarea: ['view_solicitudinterarea','change_solicitudinterarea', 'add_solicitudinterarea', 'delete_solicitudinterarea'],
            DetalleInterarea: ['view_detalleinterarea','change_detalleinterarea','add_detalleinterarea','delete_detalleinterarea'],
            InformeInterarea: ['view_informeinterarea','change_informeinterarea','add_informeinterarea','delete_informeinterarea'],
            Circuito: ['view_circuito'],
            UltimoNumero: ['view_ultimonumero'],
        }

        for model, permissions in models_permissions.items():
            content_type = ContentType.objects.get_for_model(model)
            perms = Permission.objects.filter(content_type=content_type, codename__in=permissions)
            area_jefe_group.permissions.add(*perms)

        self.stdout.write(self.style.SUCCESS('Successfully created the area_jefe group and assigned permissions'))
