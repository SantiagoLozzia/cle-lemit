import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0041_migrar_estados_descartado'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CicloInterarea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.PositiveIntegerField(default=1)),
                ('tipo', models.CharField(
                    choices=[('parcial', 'Parcial'), ('complementario', 'Complementario'), ('final', 'Final')],
                    default='parcial',
                    max_length=20,
                )),
                ('adjunto_informeArea', models.FileField(blank=True, null=True, upload_to='informes_ia_area/')),
                ('fecha_informeArea', models.DateField(blank=True, null=True)),
                ('adjunto_informeServicio', models.FileField(blank=True, null=True, upload_to='informes_ia_servicio/')),
                ('fecha_informeServicio', models.DateField(blank=True, null=True)),
                ('adjunto_informeServicio_pdf', models.FileField(blank=True, null=True, upload_to='informes_ia_pdf/')),
                ('pdf_confirmado_admin', models.BooleanField(default=False)),
                ('correcciones', models.TextField(blank=True, max_length=2500, null=True)),
                ('corregir', models.BooleanField(default=False)),
                ('revision_confirmada', models.BooleanField(default=False)),
                ('nota_rechazo_st', models.TextField(blank=True, null=True)),
                ('rechazo_st_destino', models.CharField(blank=True, max_length=20, null=True)),
                ('nota_rechazo_area', models.TextField(blank=True, null=True)),
                ('rechazo_area_destino', models.CharField(blank=True, max_length=20, null=True)),
                ('nota_rechazo_direccion', models.TextField(blank=True, null=True)),
                ('rechazo_destino', models.CharField(blank=True, max_length=20, null=True)),
                ('firma_responsable_area', models.BooleanField(default=False)),
                ('adjunto_firmado_area', models.FileField(blank=True, null=True, upload_to='informes_ia_firmados/')),
                ('firma_direccion', models.BooleanField(default=False)),
                ('adjunto_firmado_direccion', models.FileField(blank=True, null=True, upload_to='informes_ia_firmados/')),
                ('nro_solicitudInterarea', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='ciclos',
                    to='database.solicitudinterarea',
                )),
            ],
            options={
                'ordering': ['numero'],
            },
        ),
        migrations.CreateModel(
            name='RegistroEnsayoCicloIA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='registros_ensayo_ia/')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('ciclo_ia', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='registros_ensayo',
                    to='database.ciclointerarea',
                )),
            ],
            options={
                'ordering': ['fecha'],
            },
        ),
        migrations.CreateModel(
            name='CorreccionIA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(
                    choices=[('st', 'ST'), ('area', 'Área'), ('direccion', 'Dirección')],
                    max_length=20,
                )),
                ('destinatario', models.CharField(
                    choices=[('administracion', 'Administración'), ('st', 'ST'), ('area', 'Área'), ('direccion', 'Dirección')],
                    default='administracion',
                    max_length=20,
                )),
                ('descripcion', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(
                    choices=[('pendiente', 'Pendiente'), ('confirmada', 'Confirmada')],
                    default='pendiente',
                    max_length=20,
                )),
                ('ciclo_ia', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='historial_correcciones',
                    to='database.ciclointerarea',
                )),
                ('autor', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'ordering': ['fecha'],
            },
        ),
    ]
