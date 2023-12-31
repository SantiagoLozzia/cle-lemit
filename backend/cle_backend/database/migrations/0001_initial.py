# Generated by Django 4.2.7 on 2023-11-30 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataServicio',
            fields=[
                ('nro_dataServicio', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('area_tematica', models.CharField(choices=[('hormigones', 'Hormigones'), ('estudios_especiales', 'Estudios Especiales'), ('durabilidad', 'Durabilidad'), ('geologia', 'Geología'), ('patrimonio', 'Patrimonio'), ('metalurgia', 'Metalurgia'), ('tecnologia_vial', 'Tecnología Vial'), ('ensayos_mecanicos', 'Ensayos Mecánicos'), ('quimica', 'Química')])),
                ('adjunto_solicitudServicio', models.FileField(upload_to='solicitudes_servicio/')),
                ('contacto', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=20)),
                ('obra', models.CharField(max_length=255)),
                ('plazo_estimado', models.IntegerField()),
                ('cant_numLabs', models.IntegerField()),
                ('muestras', models.TextField()),
                ('observaciones', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='InformeArea',
            fields=[
                ('nro_informeArea', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('adjunto_informeServicio', models.FileField(upload_to='informes_areas/')),
            ],
        ),
        migrations.CreateModel(
            name='InformeInterarea',
            fields=[
                ('nro_informeInterarea', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('area_tematica', models.CharField(choices=[('hormigones', 'Hormigones'), ('estudios_especiales', 'Estudios Especiales'), ('durabilidad', 'Durabilidad'), ('geologia', 'Geología'), ('patrimonio', 'Patrimonio'), ('metalurgia', 'Metalurgia'), ('tecnologia_vial', 'Tecnología Vial'), ('ensayos_mecanicos', 'Ensayos Mecánicos'), ('quimica', 'Química')])),
                ('adjunto_informeInterarea', models.FileField(upload_to='informes_interarea/')),
            ],
        ),
        migrations.CreateModel(
            name='Legajo',
            fields=[
                ('nro_legajo', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('num_laboratorios', models.IntegerField()),
                ('pago', models.BooleanField()),
                ('plazo_pago', models.IntegerField(default=30)),
                ('facturaAdjunta', models.BooleanField()),
                ('adjunto_factura', models.FileField(upload_to='facturas/')),
                ('nro_dataServicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.dataservicio')),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('nro_servicio', models.AutoField(primary_key=True, serialize=False)),
                ('servicio', models.CharField(max_length=255)),
                ('norma', models.CharField(max_length=255)),
                ('arancel', models.DecimalField(decimal_places=2, max_digits=10)),
                ('area_tematica', models.CharField(choices=[('hormigones', 'Hormigones'), ('estudios_especiales', 'Estudios Especiales'), ('durabilidad', 'Durabilidad'), ('geologia', 'Geología'), ('patrimonio', 'Patrimonio'), ('metalurgia', 'Metalurgia'), ('tecnologia_vial', 'Tecnología Vial'), ('ensayos_mecanicos', 'Ensayos Mecánicos'), ('quimica', 'Química')])),
            ],
        ),
        migrations.CreateModel(
            name='Solicitante',
            fields=[
                ('nro_solicitante', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_solicitante', models.CharField(max_length=255)),
                ('cuit', models.CharField(max_length=20)),
                ('pais', models.CharField(max_length=50)),
                ('provincia', models.CharField(max_length=50)),
                ('localidad', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('codigoPostal', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='SolicitudInterarea',
            fields=[
                ('nro_solicitudInterarea', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('area_tematica', models.CharField(choices=[('hormigones', 'Hormigones'), ('estudios_especiales', 'Estudios Especiales'), ('durabilidad', 'Durabilidad'), ('geologia', 'Geología'), ('patrimonio', 'Patrimonio'), ('metalurgia', 'Metalurgia'), ('tecnologia_vial', 'Tecnología Vial'), ('ensayos_mecanicos', 'Ensayos Mecánicos'), ('quimica', 'Química')], max_length=20)),
                ('muestras_solicitudIa', models.TextField()),
                ('num_labs', models.IntegerField()),
                ('observaciones', models.TextField()),
                ('adjunto_solicitudInterarea', models.FileField(upload_to='solicitudes_interarea/')),
                ('nro_informeInterarea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.informeinterarea')),
            ],
        ),
        migrations.CreateModel(
            name='Recepcion',
            fields=[
                ('nro_recepcion', models.AutoField(primary_key=True, serialize=False)),
                ('nros_remitos', models.CharField(max_length=255)),
                ('estado_recepcion', models.CharField(choices=[(0, '0%'), (5, '5%'), (10, '10%'), (15, '15%'), (20, '20%'), (25, '25%'), (30, '30%'), (40, '40%'), (50, '50%'), (60, '60%'), (70, '70%'), (80, '80%'), (90, '90%'), (100, '100%')])),
                ('plazo_muestras', models.IntegerField(default=30)),
                ('nro_legajo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='database.legajo')),
            ],
        ),
        migrations.CreateModel(
            name='Presupuesto',
            fields=[
                ('nro_presupuesto', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('contacto', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('area_tematica', models.CharField(choices=[('hormigones', 'Hormigones'), ('estudios_especiales', 'Estudios Especiales'), ('durabilidad', 'Durabilidad'), ('geologia', 'Geología'), ('patrimonio', 'Patrimonio'), ('metalurgia', 'Metalurgia'), ('tecnologia_vial', 'Tecnología Vial'), ('ensayos_mecanicos', 'Ensayos Mecánicos'), ('quimica', 'Química')])),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('descuento', models.IntegerField(choices=[(0, '0%'), (5, '5%'), (10, '10%'), (15, '15%'), (20, '20%'), (25, '25%'), (30, '30%'), (40, '40%'), (50, '50%'), (60, '60%'), (70, '70%'), (80, '80%'), (90, '90%'), (100, '100%')])),
                ('arancel_presupuesto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('observaciones', models.TextField()),
                ('estado_presupuesto', models.CharField(max_length=50)),
                ('nro_solicitante', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='database.solicitante')),
            ],
        ),
        migrations.CreateModel(
            name='OrdenServicio',
            fields=[
                ('nro_ordenServicio', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('observaciones', models.TextField()),
                ('nro_informeArea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.informearea')),
                ('nro_legajo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.legajo')),
            ],
        ),
        migrations.AddField(
            model_name='legajo',
            name='nro_ordenServicio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.ordenservicio'),
        ),
        migrations.AddField(
            model_name='legajo',
            name='nro_recepcion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.recepcion'),
        ),
        migrations.CreateModel(
            name='InformeServicio',
            fields=[
                ('nro_informeServicio', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('adjunto_informeServicio', models.FileField(upload_to='informes_servicio/')),
                ('revision', models.BooleanField()),
                ('firma_area', models.BooleanField()),
                ('firma_direccion', models.BooleanField()),
                ('nro_informeArea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.informearea')),
            ],
        ),
        migrations.AddField(
            model_name='informeinterarea',
            name='nro_solicitudInterarea',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.solicitudinterarea'),
        ),
        migrations.AddField(
            model_name='informearea',
            name='nro_informeServicio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.informeservicio'),
        ),
        migrations.AddField(
            model_name='informearea',
            name='nro_ordenServicio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.ordenservicio'),
        ),
        migrations.AddField(
            model_name='informearea',
            name='nro_solicitud_interarea',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.solicitudinterarea'),
        ),
        migrations.CreateModel(
            name='DetallePresupuesto',
            fields=[
                ('nro_detalle', models.AutoField(primary_key=True, serialize=False)),
                ('cant', models.IntegerField()),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('nro_presupuesto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.presupuesto')),
                ('nro_servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.servicio')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleInterarea',
            fields=[
                ('nro_detalle', models.AutoField(primary_key=True, serialize=False)),
                ('nro_servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.servicio')),
                ('nro_solicitudInterarea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.solicitudinterarea')),
            ],
        ),
        migrations.AddField(
            model_name='dataservicio',
            name='nro_legajo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.legajo'),
        ),
        migrations.AddField(
            model_name='dataservicio',
            name='nro_presupuesto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.presupuesto'),
        ),
    ]
