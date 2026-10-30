from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0024_dataservicio_emails'),
    ]

    operations = [
        migrations.AddField(
            model_name='adjuntofactura',
            name='monto',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
    ]
