# Generated by Django 2.2 on 2024-11-11 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0009_model_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model',
            name='tfile_binary',
            field=models.FileField(max_length=500, upload_to='file'),
        ),
    ]
