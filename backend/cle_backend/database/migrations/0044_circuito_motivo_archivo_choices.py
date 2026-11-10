from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0043_merge_20261106_0805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='circuito',
            name='motivo_archivo',
            field=models.CharField(
                blank=True,
                choices=[
                    ('exito', 'Finalizado con éxito'),
                    ('falta_pago', 'Empresa no abonó'),
                    ('vencimiento_muestras', 'Vencimiento del plazo de muestras'),
                    ('desistimiento', 'Desistimiento del cliente'),
                    ('otro', 'Otro'),
                ],
                max_length=30,
                null=True,
            ),
        ),
    ]
