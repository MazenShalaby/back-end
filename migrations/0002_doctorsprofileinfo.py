# Generated by Django 5.1.3 on 2024-11-09 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorsProfileInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=10)),
                ('last_name', models.CharField(max_length=10)),
                ('specialty', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.PositiveIntegerField(max_length=15)),
                ('clinic_address', models.TextField()),
                ('bio', models.TextField()),
            ],
        ),
    ]
