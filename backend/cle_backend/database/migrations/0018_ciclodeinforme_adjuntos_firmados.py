from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0019_merge_0017_correccionst_0018_merge_20261023_0839'),
    ]

    operations = [
        migrations.AddField(
            model_name='cicloinforme',
            name='adjunto_firmado_area',
            field=models.FileField(blank=True, null=True, upload_to='informes_firmados/'),
        ),
        migrations.AddField(
            model_name='cicloinforme',
            name='adjunto_firmado_direccion',
            field=models.FileField(blank=True, null=True, upload_to='informes_firmados/'),
        ),
    ]
