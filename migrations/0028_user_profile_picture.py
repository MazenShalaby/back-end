# Generated by Django 5.1.4 on 2025-01-31 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customize', '0027_alarm_updated_at_alter_alarm_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=''),
        ),
    ]
