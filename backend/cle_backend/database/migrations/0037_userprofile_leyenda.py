from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0036_circuito_fecha_archivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='leyenda',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
