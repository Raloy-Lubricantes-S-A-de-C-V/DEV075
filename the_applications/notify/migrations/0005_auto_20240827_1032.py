# Generated by Django 2.2 on 2024-08-27 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notify', '0004_notify_to'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notify',
            old_name='type',
            new_name='type_id',
        ),
        migrations.RenameField(
            model_name='notify',
            old_name='user',
            new_name='user_id',
        ),
    ]
