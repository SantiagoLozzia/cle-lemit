# Generated by Django 4.2.7 on 2024-02-28 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0016_informearea_estado_informearea'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recepcion',
            name='estado_recepcion',
            field=models.CharField(choices=[('sin_llegar', 'Sin LLegar'), ('parcial', 'Parcial'), ('total', 'Total')]),
        ),
    ]