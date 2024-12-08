# Generated by Django 5.1.3 on 2024-12-06 11:52

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_alter_userprofile_choronic_disease'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='doctor',
        ),
        migrations.AlterField(
            model_name='doctorsprofileinfo',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='DoctorAvailableBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(default=datetime.datetime.now)),
                ('availability', models.BooleanField(blank=True, default=True, null=True)),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.doctorsprofileinfo')),
            ],
            options={
                'verbose_name': 'Booking',
            },
        ),
        migrations.AddField(
            model_name='appointment',
            name='available_booking',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.doctoravailablebooking'),
        ),
    ]
