# Generated by Django 5.1.4 on 2025-01-28 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customize', '0006_remove_bookedappointment_booked_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookedappointment',
            old_name='available',
            new_name='booked',
        ),
    ]
