from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0012_rename_informeparcial_informeareaparcial'),
    ]

    operations = [
        migrations.AddField(
            model_name='presupuesto',
            name='motivo_cancelacion',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
