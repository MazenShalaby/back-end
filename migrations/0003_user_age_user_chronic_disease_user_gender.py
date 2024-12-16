# Generated by Django 5.1.4 on 2024-12-16 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customize', '0002_remove_user_age_remove_user_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='chronic_disease',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=10, null=True),
        ),
    ]
