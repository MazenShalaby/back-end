# Generated by Django 5.1.4 on 2025-01-28 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customize', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctoravailability',
            name='department',
            field=models.CharField(choices=[('اخصائي سكر الاطفال', 'اخصائي سكر الاطفال'), ('اخصائي علاج طبيعي', 'اخصائي علاج طبيعي'), ('اخصائي امراض القلب', 'اخصائي امراض القلب')], max_length=100),
        ),
    ]
