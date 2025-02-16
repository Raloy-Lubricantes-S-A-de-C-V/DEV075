# Generated by Django 2.2 on 2024-10-16 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datasheet', '0004_auto_20241016_0820'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelParent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_son', models.IntegerField()),
                ('type', models.CharField(choices=[('CO', 'Copia'), ('FU', 'Fusión')], default='CO', max_length=20, verbose_name='Tipo')),
                ('write_date', models.DateTimeField(auto_now_add=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('create_uid', models.IntegerField()),
                ('write_uid', models.IntegerField()),
                ('id_parent', models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to='datasheet.Header')),
            ],
        ),
    ]
