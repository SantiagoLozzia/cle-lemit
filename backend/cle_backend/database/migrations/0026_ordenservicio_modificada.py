from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0025_adjuntofactura_monto'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordenservicio',
            name='modificada',
            field=models.BooleanField(default=False),
        ),
    ]
