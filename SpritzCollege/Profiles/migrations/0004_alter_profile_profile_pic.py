# Generated by Django 5.0.6 on 2024-06-03 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profiles', '0003_profile_interests'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(upload_to='profile_pics'),
        ),
    ]
