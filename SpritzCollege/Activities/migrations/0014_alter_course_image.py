# Generated by Django 5.0.6 on 2024-05-24 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Activities', '0013_course_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(default='Courses/default.jpg', upload_to=''),
        ),
    ]
