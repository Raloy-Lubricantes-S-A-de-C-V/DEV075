# Generated by Django 2.2 on 2024-11-10 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0008_auto_20241108_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='model',
            name='status',
            field=models.CharField(choices=[('ready', 'Listo'), ('used', 'En uso')], default='ready', max_length=20),
        ),
    ]
