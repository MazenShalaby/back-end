# Generated by Django 5.1.4 on 2025-01-31 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customize', '0026_alter_alarm_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='alarm',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='alarm',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
