# Generated by Django 5.1.4 on 2025-01-29 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customize', '0013_alter_booking_appointments_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookedappointment',
            options={},
        ),
        migrations.AlterModelOptions(
            name='doctoravailability',
            options={'verbose_name': 'Doctors Availability'},
        ),
    ]
