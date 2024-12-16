# Generated by Django 5.1.4 on 2024-12-16 14:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customize', '0010_profile_phone_num_user_phone_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_num',
            field=models.CharField(blank=True, max_length=11, null=True, validators=[django.core.validators.RegexValidator(code='invalid_phone_num', message='Phone number must be exactly 11 digits.', regex='^\\d{11}$')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_num',
            field=models.CharField(blank=True, max_length=11, null=True, validators=[django.core.validators.RegexValidator(code='invalid_phone_num', message='Phone number must be exactly 11 digits.', regex='^\\d{11}$')]),
        ),
    ]