from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from database.models import *

class Command(BaseCommand):
    help = 'Create the group direccion and assign permissions'

    def handle(self, *args, **options):
        # Crear Grupo 'direccion'
        direccion_group, created = Group.objects.get_or_create(name='direccion')

        # Asignar permisos al grupo 'direccion'
        models_permissions = {
            Solicitante: ['view_solicitante'],
            Presupuesto: ['view_presupuesto'],
            Servicio: ['view_servicio'],
            DetallePresupuesto: ['view_detallepresupuesto'],
            DataServicio: ['view_dataservicio'],
            Legajo: ['view_legajo'],
            Recepcion: ['view_recepcion'],
            OrdenServicio: ['view_ordenservicio'],
            InformeArea: ['view_informearea'],
            InformeServicio: ['view_informeservicio'],
            SolicitudInterarea: ['view_solicitudinterarea'],
            DetalleInterarea: ['view_detalleinterarea'],
            InformeInterarea: ['view_informeinterarea'],
            Circuito: ['view_circuito', 'change_circuito', 'add_circuito', 'delete_circuito'],
            UltimoNumero: ['view_ultimonumero', 'change_ultimonumero', 'add_ultimonumero', 'delete_ultimonumero'],
        }

        for model, permissions in models_permissions.items():
            content_type = ContentType.objects.get_for_model(model)
            perms = Permission.objects.filter(content_type=content_type, codename__in=permissions)
            direccion_group.permissions.add(*perms)

        self.stdout.write(self.style.SUCCESS('Successfully created the direccion group and assigned permissions'))
