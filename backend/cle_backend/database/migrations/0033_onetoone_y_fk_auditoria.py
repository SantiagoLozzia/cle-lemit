from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0032_pago_choices_string'),
    ]

    operations = [
        # DataServicio: FK -> OneToOneField
        migrations.AlterField(
            model_name='dataservicio',
            name='nro_circuito',
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='data_servicio',
                to='database.circuito',
            ),
        ),
        # Legajo: FK -> OneToOneField
        migrations.AlterField(
            model_name='legajo',
            name='nro_circuito',
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='legajo',
                to='database.circuito',
            ),
        ),
        # Recepcion: FK -> OneToOneField
        migrations.AlterField(
            model_name='recepcion',
            name='nro_circuito',
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='recepcion',
                to='database.circuito',
            ),
        ),
        # OrdenServicio: FK -> OneToOneField
        migrations.AlterField(
            model_name='ordenservicio',
            name='nro_circuito',
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='orden_servicio',
                to='database.circuito',
            ),
        ),
        # EventoAuditoria.nro_circuito: IntegerField -> FK
        migrations.AlterField(
            model_name='eventoauditoria',
            name='nro_circuito',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='eventos_auditoria',
                to='database.circuito',
            ),
        ),
    ]
