import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def migrar_correcciones_st(apps, schema_editor):
    CorreccionST = apps.get_model('database', 'CorreccionST')
    Correccion = apps.get_model('database', 'Correccion')
    for vieja in CorreccionST.objects.all():
        Correccion.objects.create(
            ciclo=vieja.ciclo,
            tipo='st',
            descripcion=vieja.descripcion,
            estado='pendiente',
            autor=None,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0028_ordenservicio_nuevo_rango_lab'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Correccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('st', 'ST'), ('area', 'Área'), ('direccion', 'Dirección')], max_length=20)),
                ('descripcion', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('confirmada', 'Confirmada')], default='pendiente', max_length=20)),
                ('ciclo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historial_correcciones', to='database.cicloinforme')),
                ('autor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['fecha']},
        ),
        migrations.RunPython(migrar_correcciones_st, migrations.RunPython.noop),
        migrations.DeleteModel(name='CorreccionST'),
    ]
