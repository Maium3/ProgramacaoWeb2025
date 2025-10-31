# Generated manual migration to add participants M2M and remove old amigo fields
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('paginas', '0010_conversausuarios_mensagemconversausuarios'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversausuarios',
            name='participants',
            field=models.ManyToManyField(related_name='conversas_participantes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='conversausuarios',
            name='amigo_username',
        ),
        migrations.RemoveField(
            model_name='conversausuarios',
            name='amigo_codigo_id',
        ),
    ]
