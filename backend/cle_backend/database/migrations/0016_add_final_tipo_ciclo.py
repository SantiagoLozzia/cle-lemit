from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0015_editar_dataservicio'),
    ]

    operations = [
        # CicloInforme and RegistroEnsayoCiclo tables already exist in the DB;
        # this SeparateDatabaseAndState block only injects them into the migration
        # state so subsequent AlterField/AddField operations can reference them.
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='CicloInforme',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('nro_circuito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ciclos', to='database.circuito')),
                        ('numero', models.PositiveIntegerField(default=1)),
                        ('tipo', models.CharField(choices=[('parcial', 'Parcial'), ('complementario', 'Complementario')], default='parcial', max_length=20)),
                        ('adjunto_informeArea', models.FileField(blank=True, null=True, upload_to='informes_area/')),
                        ('fecha_informeArea', models.DateField(blank=True, null=True)),
                        ('adjunto_informeServicio', models.FileField(blank=True, null=True, upload_to='informes_servicio/')),
                        ('fecha_informeServicio', models.DateField(blank=True, null=True)),
                        ('correcciones', models.TextField(blank=True, max_length=2500, null=True)),
                        ('corregir', models.BooleanField(default=False)),
                        ('revision_confirmada', models.BooleanField(default=False)),
                        ('firma_responsable_area', models.BooleanField(default=False)),
                        ('firma_direccion', models.BooleanField(default=False)),
                    ],
                ),
                migrations.CreateModel(
                    name='RegistroEnsayoCiclo',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('ciclo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registros_ensayo', to='database.cicloinforme')),
                        ('archivo', models.FileField(upload_to='registros_ensayo/')),
                        ('fecha', models.DateTimeField(auto_now_add=True)),
                    ],
                    options={'ordering': ['fecha']},
                ),
            ],
            database_operations=[],
        ),
        migrations.AlterField(
            model_name='cicloinforme',
            name='tipo',
            field=models.CharField(
                choices=[('parcial', 'Parcial'), ('complementario', 'Complementario'), ('final', 'Final')],
                default='parcial',
                max_length=20,
            ),
        ),
    ]
