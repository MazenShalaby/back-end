# Generated by Django 5.1.3 on 2024-12-06 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_remove_appointment_date_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctorsprofileinfo',
            old_name='first_name',
            new_name='doctorname',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='first_name',
            new_name='username',
        ),
        migrations.AlterField(
            model_name='doctorsprofileinfo',
            name='last_name',
            field=models.CharField(max_length=50),
        ),
    ]