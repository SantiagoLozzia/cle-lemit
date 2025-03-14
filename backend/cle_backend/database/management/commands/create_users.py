from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.db import IntegrityError
from database.models import UserProfile

class Command(BaseCommand):
    help = 'Create initial users and assign them to groups'

    def handle(self, *args, **options):
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

        users_data = [
            # Datos de Usuarios
            ('juan.dimaio', 'Juan', 'Di Maio', 'servicios_tecnologicos', 'servicios_tecnologicos'),
            ('jorge.coacci', 'Jorge', 'Coacci', 'servicios_tecnologicos', 'servicios_tecnologicos'),
            ('melisa.siruela', 'Melisa', 'Siruela', 'administracion', 'administracion'),
            ('julieta.schiappacasse', 'Julieta', 'Schiappacasse', 'administracion', 'administracion'),
            ('natalia.desimone', 'Natalia', 'Desimone', 'administracion', 'administracion'),
            ('fabian.iloro', 'Fabian', 'Iloro', 'direccion', 'direccion'),
            ('dario.falcone', 'Dario', 'Falcone', 'durabilidad', 'area_jefe'),
            ('lautaro.iloro', 'Lautaro', 'Iloro', 'durabilidad', 'area_standard'),
            ('gustavo.veloso', 'Gustavo', 'Veloso', 'ensayos_mecanicos', 'area_jefe'),
            ('lucas.gonzalez', 'Lucas', 'Gonzalez', 'ensayos_mecanicos', 'area_standard'),
            ('alejandro.ribot', 'Alejandro', 'Ribot', 'geologia', 'area_jefe'),
            ('marcos.panei', 'Marcos', 'Panei', 'geologia', 'area_standard'),
            ('claudio.zega', 'Claudio', 'Zega', 'hormigones', 'area_jefe'),
            ('guillermo.herrera', 'Guillermo', 'Herrera', 'hormigones', 'area_standard'),
            ('ricardo.gregorutti', 'Ricardo', 'Gregorutti', 'metalurgia', 'area_jefe'),
            ('jorge.grau', 'Jorge', 'Grau', 'metalurgia', 'area_standard'),
            ('mariana.lopez', 'Mariana', 'Lopez', 'patrimonio', 'area_jefe'),
            ('maria.di_maio', 'Maria', 'Di Maio', 'patrimonio', 'area_standard'),
            ('silvia.zicarelli', 'Silvia', 'Zicarelli', 'quimica', 'area_jefe'),
            ('claudio.veloso', 'Claudio', 'Veloso', 'tecnologia_vial', 'area_jefe'),
            ('celeste.torrijos', 'Celeste', 'Torrijos', 'estudios_especiales', 'area_jefe')
        ]

        for username, first_name, last_name, area_tematica, rol in users_data:
            try:
                # Verificar si el usuario ya existe
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={'first_name': first_name, 'last_name': last_name, 'password': 'securepassword'}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Usuario creado: {username}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Usuario ya existe: {username}'))
                
                # Crear o actualizar el perfil del usuario
                UserProfile.objects.update_or_create(
                    user=user,
                    defaults={'area_tematica': area_tematica, 'rol': rol}
                )
                
            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f'Error de integridad para el usuario {username}: {e}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error inesperado para el usuario {username}: {e}'))

        # Asignar Usuarios a los grupos
        user_groups = {
            'servicios_tecnologicos': [ 'juan.dimaio', 'jorge.coacci' ],
            'administracion': [ 'melisa.siruela', 'julieta.schiappacasse', 'natalia.desimone' ],
            'direccion': [ 'fabian.iloro' ],
            'area_jefe': [ 'dario.falcone', 'gustavo.veloso', 'alejandro.ribot', 'claudio.zega', 'ricardo.gregorutti', 'mariana.lopez', 'silvia.zicarelli', 'claudio.veloso', 'celeste.torrijos' ],
            'area_standard': [ 'lautaro.iloro', 'lucas.gonzalez', 'marcos.panei', 'guillermo.herrera', 'jorge.grau', 'maria.di_maio' ],
        }

        for area, usernames in user_groups.items():
            try:
                group = Group.objects.get(name=area)
                for username in usernames:
                    user = User.objects.get(username=username)
                    user.groups.add(group)
                    self.stdout.write(self.style.SUCCESS(f'Usuario {username} asignado al grupo {area}'))
            except Group.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Grupo no encontrado: {area}'))
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Usuario no encontrado para asignación: {username}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error inesperado al asignar usuario {username} al grupo {area}: {e}'))
