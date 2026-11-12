from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0048_remove_phantom_models_add_servicio_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudinterarea',
            name='tipo',
            field=models.CharField(
                blank=True,
                choices=[('parcial', 'Parcial'), ('resultado', 'Resultado'), ('complementario', 'Complementario')],
                default='parcial',
                max_length=20,
            ),
        ),
    ]
