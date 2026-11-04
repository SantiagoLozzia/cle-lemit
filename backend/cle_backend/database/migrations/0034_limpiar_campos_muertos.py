from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0033_onetoone_y_fk_auditoria'),
    ]

    operations = [
        # Eliminar campo muerto DataServicio.adjunto_solicitudServicio
        # (ya migrado a AdjuntoSolicitudServicio en 0014)
        migrations.RemoveField(
            model_name='dataservicio',
            name='adjunto_solicitudServicio',
        ),
        # Eliminar campo muerto Legajo.adjunto_factura
        # (ya migrado a AdjuntoFactura en 0014)
        migrations.RemoveField(
            model_name='legajo',
            name='adjunto_factura',
        ),
        # Agregar default='0' al campo pago
        migrations.AlterField(
            model_name='legajo',
            name='pago',
            field=models.CharField(
                choices=[
                    ('0', '0%'),
                    ('100', '100%'),
                    ('no_arancelado', 'No arancelado'),
                    ('pago_diferido', 'Pago diferido'),
                ],
                default='0',
            ),
        ),
    ]
