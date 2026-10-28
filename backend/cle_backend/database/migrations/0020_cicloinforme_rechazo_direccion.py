from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0019_userprofile_firma'),
    ]

    operations = [
        migrations.AddField(
            model_name='cicloinforme',
            name='nota_rechazo_direccion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cicloinforme',
            name='rechazo_destino',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
