from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0037_userprofile_leyenda'),
    ]

    operations = [
        migrations.AddField(
            model_name='presupuesto',
            name='version_formulario',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
        migrations.AddField(
            model_name='legajo',
            name='version_formulario',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
        migrations.AddField(
            model_name='ordenservicio',
            name='version_formulario',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
        migrations.CreateModel(
            name='ConfigFormulario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('presupuesto', 'Presupuesto de Servicios Tecnológicos'), ('legajo', 'Legajo'), ('orden_servicio', 'Orden de Servicio')], max_length=50, unique=True)),
                ('nombre', models.CharField(max_length=200)),
                ('codigo', models.CharField(max_length=50)),
                ('version_actual', models.CharField(default='01', max_length=10)),
            ],
            options={
                'verbose_name': 'Configuración de Formulario',
                'verbose_name_plural': 'Configuraciones de Formularios',
            },
        ),
        migrations.CreateModel(
            name='RevisionFormulario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=10)),
                ('fecha', models.DateField()),
                ('descripcion', models.TextField()),
                ('aprobado_por', models.CharField(max_length=200)),
                ('formulario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='revisiones', to='database.configformulario')),
            ],
            options={
                'verbose_name': 'Revisión de Formulario',
                'verbose_name_plural': 'Revisiones de Formularios',
                'ordering': ['version'],
            },
        ),
    ]
