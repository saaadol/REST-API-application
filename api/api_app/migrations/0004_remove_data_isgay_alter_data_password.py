# Generated by Django 5.0 on 2024-04-04 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0003_alter_data_isgay'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='isgay',
        ),
        migrations.AlterField(
            model_name='data',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
