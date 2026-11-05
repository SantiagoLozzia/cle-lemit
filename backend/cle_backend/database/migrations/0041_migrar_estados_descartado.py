from django.db import migrations


def migrar_a_descartado(apps, schema_editor):
    Presupuesto = apps.get_model('database', 'Presupuesto')
    estados_legacy = ['rechazado', 'modificado', 'actualizado']
    for presupuesto in Presupuesto.objects.filter(estado_presupuesto__in=estados_legacy):
        estado_original = presupuesto.estado_presupuesto
        presupuesto.estado_presupuesto = 'descartado'
        if not presupuesto.motivo_descarte:
            if estado_original in ('modificado', 'actualizado'):
                presupuesto.motivo_descarte = 'nuevo_presupuesto'
            else:
                presupuesto.motivo_descarte = 'otro'
        presupuesto.save()


def reverse_migrar(apps, schema_editor):
    Presupuesto = apps.get_model('database', 'Presupuesto')
    Presupuesto.objects.filter(estado_presupuesto='descartado').update(
        estado_presupuesto='rechazado'
    )


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0040_presupuesto_motivo_descarte'),
    ]

    operations = [
        migrations.RunPython(migrar_a_descartado, reverse_migrar),
    ]
