# Generated by Django 2.0.3 on 2018-05-18 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scopes', '0002_auto_20180517_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scope',
            name='name',
            field=models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='Название зоны'),
        ),
    ]
