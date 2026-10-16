import django.db.models.deletion
from django.db import migrations, models


def migrate_existing_adjuntos(apps, schema_editor):
    DataServicio = apps.get_model('database', 'DataServicio')
    Legajo = apps.get_model('database', 'Legajo')
    InformeArea = apps.get_model('database', 'InformeArea')
    AdjuntoSolicitudServicio = apps.get_model('database', 'AdjuntoSolicitudServicio')
    AdjuntoFactura = apps.get_model('database', 'AdjuntoFactura')
    RegistroEnsayo = apps.get_model('database', 'RegistroEnsayo')

    for ds in DataServicio.objects.exclude(adjunto_solicitudServicio='').exclude(adjunto_solicitudServicio__isnull=True):
        AdjuntoSolicitudServicio.objects.create(data_servicio=ds, archivo=ds.adjunto_solicitudServicio)

    for l in Legajo.objects.exclude(adjunto_factura='').exclude(adjunto_factura__isnull=True):
        AdjuntoFactura.objects.create(legajo=l, archivo=l.adjunto_factura)

    for ia in InformeArea.objects.exclude(registros_ensayo='').exclude(registros_ensayo__isnull=True):
        if ia.nro_circuito_id:
            RegistroEnsayo.objects.create(circuito_id=ia.nro_circuito_id, archivo=ia.registros_ensayo)


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0013_presupuesto_motivo_cancelacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdjuntoSolicitudServicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='solicitudes_servicio/')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('data_servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adjuntos', to='database.dataservicio')),
            ],
            options={'ordering': ['fecha']},
        ),
        migrations.CreateModel(
            name='AdjuntoFactura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='facturas/')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('legajo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adjuntos_factura', to='database.legajo')),
            ],
            options={'ordering': ['fecha']},
        ),
        migrations.CreateModel(
            name='RegistroEnsayo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='registros_ensayo/')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('circuito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registros_ensayo_items', to='database.circuito')),
            ],
            options={'ordering': ['fecha']},
        ),
        migrations.RunPython(migrate_existing_adjuntos, migrations.RunPython.noop),
    ]
