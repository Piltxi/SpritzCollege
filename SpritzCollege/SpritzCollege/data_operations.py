import random
from faker import Faker
from django.utils import timezone
from Activities.models import Event

def delete_db (): 
    Event.objects.all().delete()
    print ("-> data off")

def init_db (num_events):

    fake = Faker()
    for _ in range(num_events):

        name = fake.name() + " Event"
        description = fake.text()
        date = fake.date_time_between(start_date='-30d', end_date='+30d')
        price = random.choice([None, round(random.uniform(0.0, 100.0), 2)])
        Event.objects.create(name=name, description=description, date=date, price=price)

    print ("-> data online")