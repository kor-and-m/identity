# Generated by Django 2.0.3 on 2018-03-24 10:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scope',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Название зоны')),
                ('back_url', models.CharField(max_length=255, verbose_name='Обратный адрес зоны')),
                ('secret', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Внешний ключ')),
            ],
            options={
                'verbose_name': 'Роль',
                'verbose_name_plural': 'Роли',
            },
        ),
    ]
