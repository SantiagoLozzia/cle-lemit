from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0020_cicloinforme_rechazo_direccion'),
    ]

    operations = [
        migrations.AddField(
            model_name='cicloinforme',
            name='nota_rechazo_area',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cicloinforme',
            name='rechazo_area_destino',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
