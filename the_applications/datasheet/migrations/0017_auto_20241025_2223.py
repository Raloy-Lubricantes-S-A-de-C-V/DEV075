# Generated by Django 2.2 on 2024-10-26 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasheet', '0016_tempnextcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='relparent',
            name='name_parent',
            field=models.CharField(default=False, max_length=40, verbose_name='Folio'),
        ),
        migrations.AddField(
            model_name='relparent',
            name='name_son',
            field=models.CharField(default=False, max_length=40, verbose_name='Folio'),
        ),
    ]
