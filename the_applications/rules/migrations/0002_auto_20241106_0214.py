# Generated by Django 2.2 on 2024-11-06 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model',
            name='texternal_query',
            field=models.TextField(),
        ),
    ]
