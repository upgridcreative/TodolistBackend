# Generated by Django 4.1.2 on 2022-11-24 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_categories_on_server_creation_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='temp_id',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]
