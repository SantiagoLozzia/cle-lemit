import datetime
from django.db import migrations


FORMULARIOS_INICIALES = [
    {
        'tipo': 'presupuesto',
        'nombre': 'Presupuesto de Servicios Tecnológicos',
        'codigo': 'LEMIT-ST-01',
        'version_actual': '01',
        'revision': {
            'version': '01',
            'fecha': datetime.date(2025, 1, 1),
            'descripcion': 'Versión inicial del formulario de presupuesto.',
            'aprobado_por': 'Dirección LEMIT',
        },
    },
    {
        'tipo': 'legajo',
        'nombre': 'Legajo',
        'codigo': 'LEMIT-ST-02',
        'version_actual': '01',
        'revision': {
            'version': '01',
            'fecha': datetime.date(2025, 1, 1),
            'descripcion': 'Versión inicial del formulario de legajo.',
            'aprobado_por': 'Dirección LEMIT',
        },
    },
    {
        'tipo': 'orden_servicio',
        'nombre': 'Orden de Servicio',
        'codigo': 'LEMIT-ST-03',
        'version_actual': '01',
        'revision': {
            'version': '01',
            'fecha': datetime.date(2025, 1, 1),
            'descripcion': 'Versión inicial del formulario de orden de servicio.',
            'aprobado_por': 'Dirección LEMIT',
        },
    },
]


def seed_formularios(apps, schema_editor):
    ConfigFormulario = apps.get_model('database', 'ConfigFormulario')
    RevisionFormulario = apps.get_model('database', 'RevisionFormulario')
    Presupuesto = apps.get_model('database', 'Presupuesto')
    Legajo = apps.get_model('database', 'Legajo')
    OrdenServicio = apps.get_model('database', 'OrdenServicio')

    for item in FORMULARIOS_INICIALES:
        config, _ = ConfigFormulario.objects.get_or_create(
            tipo=item['tipo'],
            defaults={
                'nombre': item['nombre'],
                'codigo': item['codigo'],
                'version_actual': item['version_actual'],
            },
        )
        RevisionFormulario.objects.get_or_create(
            formulario=config,
            version=item['revision']['version'],
            defaults={
                'fecha': item['revision']['fecha'],
                'descripcion': item['revision']['descripcion'],
                'aprobado_por': item['revision']['aprobado_por'],
            },
        )

    # Marcar registros existentes con versión '01' (snapshot de la versión original)
    Presupuesto.objects.filter(version_formulario='').update(version_formulario='01')
    Legajo.objects.filter(version_formulario='').update(version_formulario='01')
    OrdenServicio.objects.filter(version_formulario='').update(version_formulario='01')


def remove_seed(apps, schema_editor):
    ConfigFormulario = apps.get_model('database', 'ConfigFormulario')
    ConfigFormulario.objects.filter(tipo__in=['presupuesto', 'legajo', 'orden_servicio']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0038_configformulario_revisionformulario_version_formulario'),
    ]

    operations = [
        migrations.RunPython(seed_formularios, remove_seed),
    ]
