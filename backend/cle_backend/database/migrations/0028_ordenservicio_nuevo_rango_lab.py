from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0027_legajo_monto_adicional_pendiente'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordenservicio',
            name='nuevo_rango_lab',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
