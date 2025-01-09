# Generated by Django 5.1.4 on 2025-01-02 15:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customize', '0008_alarm'),
    ]

    operations = [
        migrations.AddField(
            model_name='previoushistory',
            name='reciever',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recieved_messages', to=settings.AUTH_USER_MODEL),
        ),
    ]
