# Generated by Django 5.1.4 on 2025-01-31 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customize', '0021_alter_previoushistory_message_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='previoushistory',
            name='timestamp',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
