# Generated by Django 5.1.4 on 2025-02-26 08:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customize', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedphoto',
            name='uploader',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
