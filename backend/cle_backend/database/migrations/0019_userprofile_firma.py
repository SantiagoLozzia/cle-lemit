from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0018_ciclodeinforme_adjuntos_firmados'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='firma',
            field=models.ImageField(blank=True, null=True, upload_to='firmas_usuarios/'),
        ),
    ]
