from django.db import migrations, models


def convertir_pago_a_string(apps, schema_editor):
    Legajo = apps.get_model('database', 'Legajo')
    for legajo in Legajo.objects.all():
        pago = str(legajo.pago)
        if pago in ('0', ''):
            legajo.pago = '0'
        elif pago == '50':
            legajo.pago = '0'
        elif pago == '100':
            legajo.pago = '100'
        legajo.save(update_fields=['pago'])


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0031_eventoauditoria'),
    ]

    operations = [
        migrations.RunPython(convertir_pago_a_string, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='legajo',
            name='pago',
            field=models.CharField(
                choices=[
                    ('0', '0%'),
                    ('100', '100%'),
                    ('no_arancelado', 'No arancelado'),
                    ('pago_diferido', 'Pago diferido'),
                ],
                default='0',
            ),
        ),
    ]
