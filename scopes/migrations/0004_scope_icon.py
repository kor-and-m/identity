# Generated by Django 2.0.3 on 2018-03-25 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scopes', '0003_scope_hours_exp'),
    ]

    operations = [
        migrations.AddField(
            model_name='scope',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='scopes/icon', verbose_name='Иконка зоны'),
        ),
    ]