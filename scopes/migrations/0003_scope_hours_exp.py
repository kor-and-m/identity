# Generated by Django 2.0.3 on 2018-03-24 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scopes', '0002_auto_20180324_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='scope',
            name='hours_exp',
            field=models.SmallIntegerField(default=168, verbose_name='Часов до сгорания токена'),
        ),
    ]
