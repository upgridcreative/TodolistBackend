# Generated by Django 4.2.3 on 2023-08-01 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_categories_is_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='color',
            field=models.CharField(default='Remove later', max_length=10, null=True),
        ),
    ]
