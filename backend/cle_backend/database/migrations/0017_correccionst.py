from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0016_add_final_tipo_ciclo'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorreccionST',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('ciclo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='correcciones_st', to='database.cicloinforme')),
            ],
            options={
                'ordering': ['fecha'],
            },
        ),
    ]
