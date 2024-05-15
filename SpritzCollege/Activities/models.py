from django.db import models
from django.utils import timezone

class Event (models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    
    date = models.DateField()
    price = models.FloatField(null=True, blank=True, default="conference room")

    place = models.CharField(max_length=20)

    def is_free(self):
        return self.price is None or self.price == 0.0

    def __str__(self):
        return self.name

class Course (models.Model):

    CATEGORY_CHOICES = [
        ('ANY', 'uncategorized'),
        ('TCH', 'tech course'),
        ('LTR', 'literature course'),
        ('LAN', 'language course'),
        ('HND', 'craftsman course'),
        ('ART', 'art course'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    start_date = models.DateField()
    end_date = models.DateField()
    recurrence_day = models.CharField(max_length=20)
    
    image = models.ImageField(upload_to='Courses', default='Courses/default.jpg')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='ANY')

    def __str__(self):
        return self.name