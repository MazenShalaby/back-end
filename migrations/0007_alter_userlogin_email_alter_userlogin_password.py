# Generated by Django 5.1.4 on 2025-01-01 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customize', '0006_alter_appointment_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlogin',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='userlogin',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
