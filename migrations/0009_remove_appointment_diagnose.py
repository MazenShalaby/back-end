# Generated by Django 5.1.3 on 2024-11-09 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_appointment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='diagnose',
        ),
    ]
