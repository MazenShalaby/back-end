# Generated by Django 5.1.4 on 2025-01-29 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customize', '0009_doctoravailability_end_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking_appointments',
            name='available',
        ),
    ]
