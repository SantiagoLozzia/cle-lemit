from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0017_correccionst'),
    ]

    operations = [
        migrations.AddField(
            model_name='ciclodeinforme',
            name='adjunto_firmado_area',
            field=models.FileField(blank=True, null=True, upload_to='informes_firmados/'),
        ),
        migrations.AddField(
            model_name='ciclodeinforme',
            name='adjunto_firmado_direccion',
            field=models.FileField(blank=True, null=True, upload_to='informes_firmados/'),
        ),
    ]
