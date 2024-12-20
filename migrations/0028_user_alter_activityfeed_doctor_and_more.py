# Generated by Django 5.1.3 on 2024-12-07 13:48

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0027_activityfeed_updated'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('national_id', models.CharField(max_length=14, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='activityfeed',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.doctorsprofileinfo'),
        ),
        migrations.AlterField(
            model_name='activityfeed',
            name='msg',
            field=models.TextField(default=None),
        ),
        migrations.CreateModel(
            name='UploadedPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='uploaded_photos/')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('uploader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.user')),
            ],
        ),
        migrations.CreateModel(
            name='PreviousHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messages', to='base.user')),
            ],
        ),
    ]
