# Generated by Django 4.2.7 on 2024-10-02 20:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0010_informeparcial'),
    ]

    operations = [
        migrations.AddField(
            model_name='informeparcial',
            name='nro_circuito',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.circuito'),
        ),
    ]
