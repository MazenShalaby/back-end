# Generated by Django 5.1.4 on 2025-01-31 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customize', '0023_alter_previoushistory_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedphoto',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
