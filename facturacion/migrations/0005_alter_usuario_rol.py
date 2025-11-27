

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0004_remove_usuario_n_documento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='rol',
            field=models.CharField(choices=[('administrador', 'Administrador'), ('vendedor', 'Vendedor')], default='vendedor', max_length=20),
        ),
    ]
