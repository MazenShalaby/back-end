# Generated by Django 5.1.4 on 2025-01-29 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customize', '0015_alter_doctoravailability_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking_appointments',
            name='date_time',
        ),
        migrations.AddField(
            model_name='booking_appointments',
            name='date',
            field=models.DateField(default=None),
        ),
        migrations.AddField(
            model_name='booking_appointments',
            name='time',
            field=models.DateField(default=None),
        ),
    ]
