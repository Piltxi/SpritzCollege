from django.db import models

class Event (models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    
    date = models.DateField()
    price = models.FloatField(null=True, blank=True)

    def is_free(self):
        return self.price is None or self.price == 0.0

    def __str__(self):
        return self.name

class Course (models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    recurrence_day = models.CharField(max_length=20)

    def __str__(self):
        return self.name
