from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0015_editar_dataservicio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cicloinforme',
            name='tipo',
            field=models.CharField(
                choices=[('parcial', 'Parcial'), ('complementario', 'Complementario'), ('final', 'Final')],
                default='parcial',
                max_length=20,
            ),
        ),
    ]
