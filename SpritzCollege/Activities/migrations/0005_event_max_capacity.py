# Generated by Django 5.0.6 on 2024-05-16 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Activities', '0004_course_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='max_capacity',
            field=models.IntegerField(default=100),
        ),
    ]