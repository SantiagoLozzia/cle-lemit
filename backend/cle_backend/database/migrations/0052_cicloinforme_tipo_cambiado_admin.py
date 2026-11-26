from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0051_ciclointerarea_firma_responsable_ap'),
    ]

    operations = [
        migrations.AddField(
            model_name='cicloinforme',
            name='tipo_cambiado_admin',
            field=models.BooleanField(default=False),
        ),
    ]
