from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from database.models import *  # Asegúrate de que este import esté correcto y que todos los modelos estén importados correctamente

class Command(BaseCommand):
    help = 'Create the group servicios_tecnologicos and assign permissions'

    def handle(self, *args, **options):
        # Crear el grupo 'servicios_tecnologicos' si no existe
        servicios_tecnologicos_group, created = Group.objects.get_or_create(name='servicios_tecnologicos')

        # Definir los permisos que se asignarán al grupo
        models_permissions = {
            Solicitante: ['view_solicitante'],
            Presupuesto: ['view_presupuesto', 'change_presupuesto', 'add_presupuesto', 'delete_presupuesto'],
            Servicio: ['view_servicio', 'change_servicio', 'add_servicio', 'delete_servicio'],
            DetallePresupuesto: ['view_detallepresupuesto', 'change_detallepresupuesto', 'add_detallepresupuesto', 'delete_detallepresupuesto'],
            DataServicio: ['view_dataservicio', 'change_dataservicio', 'add_dataservicio', 'delete_dataservicio'],
            Legajo: ['view_legajo'],
            Recepcion: ['view_recepcion', 'change_recepcion', 'add_recepcion', 'delete_recepcion'],
            OrdenServicio: ['view_ordenservicio', 'change_ordenservicio', 'add_ordenservicio', 'delete_ordenservicio'],
            InformeArea: ['view_informearea'],
            InformeServicio: ['view_informeservicio', 'change_informeservicio'],
            SolicitudInterarea: ['view_solicitudinterarea'],
            DetalleInterarea: ['view_detalleinterarea'],
            InformeInterarea: ['view_informeinterarea'],
            Circuito: ['view_circuito', 'change_circuito', 'add_circuito', 'delete_circuito'],
            UltimoNumero: ['view_ultimonumero', 'change_ultimonumero', 'add_ultimonumero', 'delete_ultimonumero'],
        }

        # Asignar permisos al grupo
        for model, permissions in models_permissions.items():
            content_type = ContentType.objects.get_for_model(model)
            perms = Permission.objects.filter(content_type=content_type, codename__in=permissions)
            servicios_tecnologicos_group.permissions.add(*perms)

        self.stdout.write(self.style.SUCCESS('Successfully created the servicios_tecnologicos group and assigned permissions'))
