# Generated by Django 5.1.5 on 2025-01-20 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notify', '0011_auto_20241111_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notify',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='typenotify',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
