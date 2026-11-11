from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0045_alter_ciclointerarea_id_alter_correccion_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudinterarea',
            name='genera_informe_parcial',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='solicitudinterarea',
            name='confirmado_area_principal',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='solicitudinterarea',
            name='comentario_rechazo_ap',
            field=models.TextField(blank=True, null=True),
        ),
    ]
