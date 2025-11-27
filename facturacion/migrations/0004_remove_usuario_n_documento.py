

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0003_add_user_onetoone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='n_documento',
        ),
    ]
