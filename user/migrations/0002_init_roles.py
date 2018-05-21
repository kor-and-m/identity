from django.db import migrations
from user.models import User, Role
 

def init_group(*_args, **_kwargs):
    Role.objects.create(name='admin', description='admin')
    Role.objects.create(name='staff', description='staff')


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(init_group)
    ]
