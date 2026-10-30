from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0026_ordenservicio_modificada'),
    ]

    operations = [
        migrations.AddField(
            model_name='legajo',
            name='monto_adicional_pendiente',
            field=models.BooleanField(default=False),
        ),
    ]
