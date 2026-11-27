from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0052_cicloinforme_tipo_cambiado_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordenservicio',
            name='max_parciales',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ordenservicio',
            name='plazos_parciales',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
