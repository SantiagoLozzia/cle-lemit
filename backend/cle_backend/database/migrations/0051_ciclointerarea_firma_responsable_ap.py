from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0050_conceptofacturacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='ciclointerarea',
            name='firma_responsable_ap',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ciclointerarea',
            name='adjunto_firmado_ap',
            field=models.FileField(blank=True, null=True, upload_to='informes_ia_firmados/'),
        ),
    ]
