# Generated by Django 5.1.4 on 2024-12-17 10:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customize', '0002_remove_doctorsprofileinfo_doctor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorsprofileinfo',
            name='phone',
            field=models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(message='Phone number must consist of exactly 11 digits.', regex='^\\d{11}$')]),
        ),
    ]
