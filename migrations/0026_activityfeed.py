# Generated by Django 5.1.3 on 2024-12-06 18:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0025_delete_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityFeed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg', models.TextField(null=True)),
                ('complete', models.BooleanField(default=False)),
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.doctorsprofileinfo')),
            ],
        ),
    ]
