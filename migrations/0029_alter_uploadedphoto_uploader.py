# Generated by Django 5.1.3 on 2024-12-07 14:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0028_user_alter_activityfeed_doctor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedphoto',
            name='uploader',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.user'),
        ),
    ]