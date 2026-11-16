from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0049_solicitudinterarea_tipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConceptoFacturacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Concepto de Facturación',
                'verbose_name_plural': 'Conceptos de Facturación',
                'ordering': ['nombre'],
            },
        ),
        migrations.AddField(
            model_name='dataservicio',
            name='conceptos_facturacion',
            field=models.ManyToManyField(blank=True, related_name='data_servicios', to='database.conceptofacturacion'),
        ),
    ]
