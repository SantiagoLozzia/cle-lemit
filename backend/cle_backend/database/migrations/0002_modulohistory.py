# Generated by Django 4.2.7 on 2024-07-24 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModuloHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.IntegerField()),
                ('fecha_cambio', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
