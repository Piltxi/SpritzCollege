# Generated by Django 5.0.6 on 2024-05-24 00:32

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Activities', '0010_alter_event_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
