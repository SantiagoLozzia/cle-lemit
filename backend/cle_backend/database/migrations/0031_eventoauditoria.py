from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0030_correccion_destinatario'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventoAuditoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accion', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=500)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('nro_circuito', models.IntegerField(blank=True, null=True)),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='eventos_auditoria', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Evento de Auditoría',
                'verbose_name_plural': 'Eventos de Auditoría',
                'ordering': ['-fecha'],
            },
        ),
    ]
