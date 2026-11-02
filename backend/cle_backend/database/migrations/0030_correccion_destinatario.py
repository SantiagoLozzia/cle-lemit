from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0029_correccion'),
    ]

    operations = [
        migrations.AddField(
            model_name='correccion',
            name='destinatario',
            field=models.CharField(
                choices=[
                    ('administracion', 'Administración'),
                    ('st', 'ST'),
                    ('area', 'Área'),
                    ('direccion', 'Dirección'),
                ],
                default='administracion',
                max_length=20,
            ),
        ),
    ]
