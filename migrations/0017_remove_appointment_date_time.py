# Generated by Django 5.1.3 on 2024-12-06 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_remove_appointment_doctor_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='date_time',
        ),
    ]
