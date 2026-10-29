from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0022_cicloinforme_pdf_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='cicloinforme',
            name='nota_rechazo_st',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cicloinforme',
            name='rechazo_st_destino',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
