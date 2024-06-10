import random
from django.apps import apps
from faker import Faker
from django.utils import timezone
from decimal import Decimal
import json
from datetime import datetime
from django.contrib.auth.models import Group
import pytz
from threading import Timer

from Activities.models import Event, Course

def db_pialla (): 
    all_models = apps.get_models()
    for model in all_models:
            model_name = model.__name__
            try:
                model.objects.all().delete()
                print(f'All data from {model_name} deleted')
            except Exception as e:
                print(f'Failed delete data from {model_name}')

    print('All data has been successfully deleted')

def db_test_events_booking (): 
    timezone = pytz.timezone('Europe/Rome')
    ev1 = Event.objects.create(
            name="Event Test 1",
            date = datetime(year=2024, month=6, day=12, hour=8, minute=31, tzinfo=timezone),
            place="conference room",
            description = "ev1 for booking test",
            price=Decimal('0.00')
        )
    
    ev2 = Event.objects.create(
            name="Event Test 2",
            date = datetime(year=2024, month=6, day=12, hour=8, minute=31, tzinfo=timezone),
            price=Decimal('0.00'),
            description = "ev2 for booking test",
            place="cinema"
        )

    print ("-> load events for booking test")

def db_create_groups ():
    group_names = ['administration', 'culture', 'visitors']

    for name in group_names:
        Group.objects.get_or_create(name=name)
    
    print ("-> create users groups")

def load_courses_from_json (file_path):
    with open(file_path, 'r') as file:
        courses_data = json.load(file)
        for course_data in courses_data:
            start_date = datetime.strptime(course_data['start_date'], '%Y-%m-%dT%H:%M:%S')
            end_date = datetime.strptime(course_data['end_date'], '%Y-%m-%dT%H:%M:%S')
            
            course = Course(
                name=course_data['name'],
                description=course_data['description'],
                start_date=start_date,
                end_date=end_date,
                recurrence_day=course_data['recurrence_day']
            )
            course.save()

def db_delete (): 
    Event.objects.all().delete()
    Course.objects.all().delete()
    print ("-> data off")

def load_events_from_json(file_path):
    with open(file_path, 'r') as file:
        events_data = json.load(file)
        for event_data in events_data:
            date_str = event_data['date']
            date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f')
            event = Event(
                name=event_data['name'],
                description=event_data['description'],
                date=date,
                price=event_data['price']
            )
            event.save()

def db_checkStatus_scheduledEvent():
    
    '''
        print("Creating test event...")
        tt = pytz.timezone('Europe/Rome')
        Event.objects.create(
            name="Event Test 1",
            date=datetime(year=2024, month=6, day=12, hour=8, minute=31, tzinfo=tt),
            place="cinema",
            description="ev for trigger test",
            price=Decimal('0.00')
        )
        print("Test event created.")
        
        testing scopes
    '''
    
    # print("Checking status of active events...")
    now = timezone.now()
    active_events = Event.objects.filter(status=Event.ACTIVE)
    print(f"CH_SCHEDULE: Active events count: {active_events.count()}")

    for ev in active_events:
        if ev.date < now:
            ev.status = Event.COMPLETED
            ev.save()
            print(f"Event {ev.name} status updated.")

    Timer(3600, db_checkStatus_scheduledEvent).start()

def _start_SpritzCollege (): 
    db_create_groups()

