from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0034_limpiar_campos_muertos'),
    ]

    operations = [
        migrations.AddField(
            model_name='circuito',
            name='motivo_archivo',
            field=models.CharField(
                blank=True,
                choices=[
                    ('exito', 'Finalizado con éxito'),
                    ('falta_pago', 'Empresa no abonó'),
                    ('vencimiento_muestras', 'Vencimiento del plazo de muestras'),
                    ('vencimiento_informe', 'Vencimiento del plazo de informe de área'),
                    ('desistimiento', 'Desistimiento del cliente'),
                    ('otro', 'Otro'),
                ],
                max_length=30,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='circuito',
            name='nota_archivo',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
