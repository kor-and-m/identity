# Generated by Django 2.0.3 on 2018-05-26 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scopes', '0003_auto_20180518_0828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scope',
            name='icon',
            field=models.ImageField(blank=True, height_field=800, null=True, upload_to='scopes/icon', verbose_name='Иконка зоны', width_field=1200),
        ),
    ]