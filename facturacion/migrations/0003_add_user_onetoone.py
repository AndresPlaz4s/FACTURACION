
from django.db import migrations, models
from django.conf import settings
from django.db import migrations



def forwards(apps, schema_editor):
    Usuario = apps.get_model('facturacion', 'Usuario')
    User = apps.get_model(settings.AUTH_USER_MODEL.split('.')[0], settings.AUTH_USER_MODEL.split('.')[1])
    for u in Usuario.objects.all():
        if u.email:
            try:
                usr = User.objects.filter(email=u.email).first()
            except Exception:
                usr = None
            if usr:
                u.user_id = usr.pk
                u.save()


def backwards(apps, schema_editor):
    Usuario = apps.get_model('facturacion', 'Usuarios')
    for u in Usuario.objects.all():
        u.user_id = None
        u.save()


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0002_alter_producto_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=models.SET_NULL, related_name='perfil_usuario', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunPython(forwards, backwards),
    ]




