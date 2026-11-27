from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0053_ordenservicio_parciales_config'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudinterarea',
            name='plazo',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
