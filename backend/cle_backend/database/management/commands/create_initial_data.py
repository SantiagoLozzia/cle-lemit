from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from solicitantes.models import Solicitante
from presupuestos.models import Presupuesto, Servicio, DetallePresupuesto, DataServicio, Legajo, Recepcion, OrdenServicio, InformeArea, InformeServicio, SolicitudInterarea, DetalleInterarea, InformeInterarea, Circuito, UltimoNumero

class Command(BaseCommand):
    help = 'Create initial users, groups, and permissions'

    def handle(self, *args, **options):
        # Crear Grupo 'servicios_tecnologicos'
        servicios_tecnologicos_group, created = Group.objects.get_or_create(name='servicios_tecnologicos')

        # Asignar permisos al grupo 'servicios_tecnologicos'
        # Modelo: Solicitante (leer)
        content_type = ContentType.objects.get_for_model(Solicitante)
        permisos = Permission.objects.filter(content_type=content_type, codename__in=[
            'view_solicitante'
        ])
        servicios_tecnologicos_group.permissions.add(*permisos)

        # Modelo: Presupuesto (todos los permisos)
        content_type = ContentType.objects.get_for_model(Presupuesto)
        permisos = Permission.objects.filter(content_type=content_type)
        servicios_tecnologicos_group.permissions.add(*permisos)

        # Modelo: Servicio (todos los permisos)
        content_type = ContentType.objects.get_for_model(Servicio)
        permisos = Permission.objects.filter(content_type=content_type)
        servicios_tecnologicos_group.permissions.add(*permisos)

        # Modelo: DetallePresupuesto (todos los permisos)
        content_type = ContentType.objects.get_for_model(DetallePresupuesto)
        permisos = Permission.objects.filter(content_type=content_type)
        servicios_tecnologicos_group.permissions.add(*permisos)

        # Modelo: DataServicio (todos los permisos)
        content_type = ContentType.objects.get_for_model(DataServicio)
        permisos = Permission.objects.filter(content_type=content_type)
        servicios_tecnologicos_group.permissions.add(*permisos)

        # Modelo: Legajo (leer)
        content_type = ContentType.objects.get_for_model(Legajo)
        permisos = Permission.objects.filter(content_type=content_type, codename__in=[
            'view_legajo'
        ])
        servicios_tecnologicos_group.permissions.add(*permisos)

        # Modelo: Recepcion (todos los permisos)
        content_type = ContentType.objects.get_for_model(Recepcion)
        permisos = Permission.objects.filter(content_type=content_type)
        servicios_tecnologicos_group.permissions.add(*permisos)

        # Modelo: OrdenServicio (todos los permisos)
        content_type = ContentType.objects.get_for_model(OrdenServicio)
        permisos = Permission.objects.filter(content_type=content_type)
        servicios_tecnologicos_group.permissions.add(*permisos)

        # Modelo: InformeArea (leer)
        content_type = ContentType.objects.get_for_model(InformeArea)
        permisos = Permission.objects.filter(content_type=content_type, codename__in=[
            'view_informearea'
        ])
        servicios_tecnologicos_group.permissions.add(*permisos)

        # Modelo: InformeServicio (leer y editar 'revision')
        content_type = ContentType.objects.get_for_model(InformeServicio)
        permisos = Permission.objects.filter(content_type=content_type, codename__in=[
            'view_informeservicio', 'change_informeservicio'
        ])
        servicios_tecnologicos_group.permissions.add(*permisos)

        # Modelo: SolicitudInterarea (leer)
        content_type = ContentType.objects.get_for_model(SolicitudInterarea)
        permisos = Permission.objects.filter(content_type=content_type, codename__in=[
            'view_solicitudinterarea'
        ])
        servicios_tecnologicos_group.permissions.add(*permisos)

        # Modelo: DetalleInterarea (leer)
        content_type = ContentType.objects.get_for_model(DetalleInterarea)
        permisos = Permission.objects.filter(content_type=content_type, codename__in=[
            'view_detalleinterarea'
        ])
        servicios_tecnologicos_group.permissions.add(*permisos)

        # Modelo: InformeInterarea (leer)
        content_type = ContentType.objects.get_for_model(InformeInterarea)
        permisos = Permission.objects.filter(content_type=content_type, codename__in=[
            'view_informeinterarea'
        ])
        servicios_tecnologicos_group.permissions.add(*permisos)

        # Modelo: Circuito (todos los permisos)
        content_type = ContentType.objects.get_for_model(Circuito)
        permisos = Permission.objects.filter(content_type=content_type)
        servicios_tecnologicos_group.permissions.add(*permisos)

        # Modelo: UltimoNumero (todos los permisos)
        content_type = ContentType.objects.get_for_model(UltimoNumero)
        permisos = Permission.objects.filter(content_type=content_type)
        servicios_tecnologicos_group.permissions.add(*permisos)

        # Crear Usuarios
        di_maio_juan = User.objects.create_user(username='juan.dimaio', first_name='Juan', last_name='Di Maio', password='password')
        coacci_jorge = User.objects.create_user(username='jorge.coacci', first_name='Jorge', last_name='Coacci', password='password')

        # Asignar Usuarios al Grupo
        di_maio_juan.groups.add(servicios_tecnologicos_group)
        coacci_jorge.groups.add(servicios_tecnologicos_group)

        self.stdout.write(self.style.SUCCESS('Successfully created initial users, groups, and permissions'))
