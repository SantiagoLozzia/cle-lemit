# Generated by Django 4.2.7 on 2024-09-23 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0006_informeservicio_revisiones'),
    ]

    operations = [
        migrations.AddField(
            model_name='informeservicio',
            name='corregir',
            field=models.BooleanField(default=False),
        ),
    ]
