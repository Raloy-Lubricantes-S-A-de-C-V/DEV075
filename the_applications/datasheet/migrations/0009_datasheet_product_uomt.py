# Generated by Django 2.2 on 2024-10-17 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasheet', '0008_auto_20241017_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='datasheet',
            name='product_uomt',
            field=models.CharField(default='', max_length=20, verbose_name='UOM T'),
        ),
    ]
