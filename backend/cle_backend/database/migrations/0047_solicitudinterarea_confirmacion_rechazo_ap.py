from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0046_solicitudinterarea_genera_informe_parcial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitudinterarea',
            name='confirmado_area_principal',
        ),
        migrations.AddField(
            model_name='solicitudinterarea',
            name='confirmado_ap',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='solicitudinterarea',
            name='tipo_rechazo_ap',
            field=models.CharField(
                blank=True,
                choices=[('informe', 'Informe'), ('registros_ensayo', 'Registros de ensayo'), ('ambos', 'Ambos')],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='solicitudinterarea',
            name='estado_correc_informe',
            field=models.CharField(
                blank=True,
                choices=[('rechazado', 'Rechazado'), ('subido', 'Subido'), ('confirmado', 'Confirmado')],
                max_length=15,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='solicitudinterarea',
            name='estado_correc_registros',
            field=models.CharField(
                blank=True,
                choices=[('rechazado', 'Rechazado'), ('subido', 'Subido'), ('confirmado', 'Confirmado')],
                max_length=15,
                null=True,
            ),
        ),
    ]
