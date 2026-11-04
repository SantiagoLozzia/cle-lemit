from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0035_circuito_motivo_archivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='circuito',
            name='fecha_archivo',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
