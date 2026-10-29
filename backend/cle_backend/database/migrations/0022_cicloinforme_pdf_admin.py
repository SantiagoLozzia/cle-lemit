from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0021_cicloinforme_rechazo_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='cicloinforme',
            name='adjunto_informeServicio_pdf',
            field=models.FileField(blank=True, null=True, upload_to='informes_servicio_pdf/'),
        ),
        migrations.AddField(
            model_name='cicloinforme',
            name='pdf_confirmado_admin',
            field=models.BooleanField(default=False),
        ),
    ]
