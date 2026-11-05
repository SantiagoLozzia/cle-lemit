from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0039_seed_config_formulario'),
    ]

    operations = [
        migrations.AddField(
            model_name='presupuesto',
            name='motivo_descarte',
            field=models.CharField(
                blank=True,
                choices=[
                    ('nuevo_presupuesto', 'Se generó un nuevo presupuesto'),
                    ('rechazo', 'Rechazado por el cliente'),
                    ('sin_respuesta', 'Sin respuesta del cliente'),
                    ('otro', 'Otro'),
                ],
                default='',
                max_length=50,
            ),
        ),
    ]
