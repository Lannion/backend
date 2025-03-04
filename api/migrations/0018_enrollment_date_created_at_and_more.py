# Generated by Django 5.1.3 on 2025-01-08 06:58

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_alter_enrollment_date_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment_date',
            name='created_at',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='enrollment_date',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
