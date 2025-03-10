# Generated by Django 5.1.3 on 2024-12-06 13:18

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_rename_first_name_doctorsprofileinfo_doctorname_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctorsprofileinfo',
            old_name='doctorname',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='doctoravailablebooking',
            name='date_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
