from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0023_cicloinforme_rechazo_st'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataservicio',
            name='email_factura',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='dataservicio',
            name='email_informe_tecnico',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
    ]
