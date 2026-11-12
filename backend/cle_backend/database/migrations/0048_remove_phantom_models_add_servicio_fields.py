from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Los modelos InformeArea, InformeAreaParcial, InformeServicio y RegistroEnsayo
    existían en el historial de migraciones previas pero sus tablas nunca se crearon
    en la DB de producción. Los campos categoria/subcategoria de Servicio también
    fueron creados por migraciones del stash aplicadas directamente. Se usa
    SeparateDatabaseAndState para todo: sólo actualizar el estado Django, sin DDL.
    """

    dependencies = [
        ('database', '0047_solicitudinterarea_confirmacion_rechazo_ap'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                # Eliminar modelos fantasma (tablas no existen en la DB)
                migrations.RemoveField(model_name='informeareaparcial', name='informe_area'),
                migrations.RemoveField(model_name='informeareaparcial', name='nro_circuito'),
                migrations.RemoveField(model_name='informeservicio', name='nro_circuito'),
                migrations.RemoveField(model_name='registroensayo', name='circuito'),
                migrations.DeleteModel(name='InformeArea'),
                migrations.DeleteModel(name='InformeAreaParcial'),
                migrations.DeleteModel(name='InformeServicio'),
                migrations.DeleteModel(name='RegistroEnsayo'),
                migrations.AlterModelOptions(
                    name='cicloinforme',
                    options={'ordering': ['numero']},
                ),
                migrations.AlterField(
                    model_name='cicloinforme',
                    name='id',
                    field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
                ),
                migrations.AlterField(
                    model_name='registroensayociclo',
                    name='id',
                    field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
                ),
                # Campos de Servicio ya existen en la DB (creados por migraciones del stash)
                migrations.AddField(
                    model_name='servicio',
                    name='categoria',
                    field=models.CharField(blank=True, default='', max_length=150),
                ),
                migrations.AddField(
                    model_name='servicio',
                    name='subcategoria',
                    field=models.CharField(blank=True, default='', max_length=150),
                ),
                migrations.AlterField(
                    model_name='servicio',
                    name='norma',
                    field=models.CharField(blank=True, default='', max_length=255),
                ),
                migrations.AlterField(
                    model_name='ultimonumero',
                    name='anio',
                    field=models.IntegerField(default=2026),
                ),
            ],
            database_operations=[],
        ),
    ]
