# Generated by Django 2.2 on 2024-11-08 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0006_auto_20241107_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='model',
            name='delete',
            field=models.SmallIntegerField(default=1),
        ),
    ]
