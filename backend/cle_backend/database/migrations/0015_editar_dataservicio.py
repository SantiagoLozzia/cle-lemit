from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0014_add_adjunto_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='legajo',
            name='labs_adicionales_pendientes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dataservicio',
            name='presupuestos_adicionales',
            field=models.ManyToManyField(
                blank=True,
                related_name='data_servicios_adicionales',
                to='database.presupuesto',
            ),
        ),
    ]
