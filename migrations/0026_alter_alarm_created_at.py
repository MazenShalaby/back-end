# Generated by Django 5.1.4 on 2025-01-31 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customize', '0025_alter_uploadedphoto_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alarm',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
