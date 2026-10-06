import json
import os

from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from database.models import UserProfile


class Command(BaseCommand):
    help = (
        'Crea usuarios iniciales y los asigna a grupos. '
        'Los datos se leen de USERS_DATA_FILE (variable de entorno) que apunta a un '
        'archivo JSON con la estructura descrita en users_data.example.json.'
    )

    def handle(self, *args, **options):
        users_data_path = os.environ.get('USERS_DATA_FILE', '').strip()
        if not users_data_path:
            raise CommandError(
                'La variable de entorno USERS_DATA_FILE no está configurada. '
                'Debe apuntar a un archivo JSON con los datos de usuarios. '
                'Consulte users_data.example.json para el formato esperado.'
            )

        try:
            with open(users_data_path, 'r', encoding='utf-8') as f:
                raw = json.load(f)
        except FileNotFoundError:
            raise CommandError(f'Archivo no encontrado: {users_data_path}')
        except json.JSONDecodeError as exc:
            raise CommandError(f'Error al parsear {users_data_path}: {exc}')

        try:
            users_data = [
                (
                    entry['username'],
                    entry['first_name'],
                    entry['last_name'],
                    entry['area_tematica'],
                    entry['rol'],
                )
                for entry in raw
            ]
        except (KeyError, TypeError) as exc:
            raise CommandError(
                f'Formato inválido en {users_data_path}. '
                f'Consulte users_data.example.json. Error: {exc}'
            )

        # Obtener los grupos
        try:
            servicios_tecnologicos_group = Group.objects.get(name='servicios_tecnologicos')
            administracion_group = Group.objects.get(name='administracion')
            direccion_group = Group.objects.get(name='direccion')
            area_jefe_group = Group.objects.get(name='area_jefe')
            area_standard_group = Group.objects.get(name='area_standard')
        except Group.DoesNotExist as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
            return

        for username, first_name, last_name, area_tematica, rol in users_data:
            try:
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={'first_name': first_name, 'last_name': last_name}
                )
                if created:
                    user.set_unusable_password()
                    user.save(update_fields=['password'])
                    self.stdout.write(self.style.SUCCESS(f'Usuario creado: {username}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Usuario ya existe: {username}'))

                UserProfile.objects.update_or_create(
                    user=user,
                    defaults={'area_tematica': area_tematica, 'rol': rol}
                )

            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f'Error de integridad para el usuario {username}: {e}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error inesperado para el usuario {username}: {e}'))

        # Asignar usuarios a grupos según el rol
        rol_to_group = {
            'servicios_tecnologicos': servicios_tecnologicos_group,
            'administracion': administracion_group,
            'direccion': direccion_group,
            'area_jefe': area_jefe_group,
            'area_standard': area_standard_group,
        }

        for username, _, _, _, rol in users_data:
            group = rol_to_group.get(rol)
            if not group:
                self.stdout.write(self.style.WARNING(f'Rol desconocido "{rol}" para {username}, no se asignó grupo.'))
                continue
            try:
                user = User.objects.get(username=username)
                user.groups.add(group)
                self.stdout.write(self.style.SUCCESS(f'Usuario {username} asignado al grupo {rol}'))
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Usuario no encontrado para asignación: {username}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error al asignar {username} al grupo {rol}: {e}'))
