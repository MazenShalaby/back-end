# Generated by Django 5.1.3 on 2024-12-06 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0024_alter_appointment_date_time'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
    ]
