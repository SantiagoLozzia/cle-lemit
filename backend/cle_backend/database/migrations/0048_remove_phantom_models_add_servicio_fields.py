from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Los modelos InformeArea, InformeAreaParcial, InformeServicio y RegistroEnsayo
    existían en el historial de migraciones previas pero sus tablas nunca se crearon
    en la DB de producción. Se usan SeparateDatabaseAndState para eliminarlos del
    estado Django sin intentar DROP TABLE.
    """

    dependencies = [
        ('database', '0047_solicitudinterarea_confirmacion_rechazo_ap'),
    ]

    operations = [
        # Eliminar modelos fantasma del estado Django únicamente (las tablas no existen en la DB)
        migrations.SeparateDatabaseAndState(
            state_operations=[
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
            ],
            database_operations=[],
        ),

        # Campos reales nuevos en Servicio
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
    ]
