# Generated by Django 2.2 on 2024-08-27 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notify', '0003_notify_see'),
    ]

    operations = [
        migrations.AddField(
            model_name='notify',
            name='to',
            field=models.SmallIntegerField(default=1),
        ),
    ]
