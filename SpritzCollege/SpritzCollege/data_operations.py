import random
from faker import Faker
from django.utils import timezone
from decimal import Decimal
import json
from datetime import datetime
from django.contrib.auth.models import Group
import pytz

from Activities.models import Event, Course

def test_eventsbooking (): 
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

def create_user_groups ():
    # directors, administration, culture, students, visitors, maintainers
    group_names = ['directors', 'administration', 'culture', 'students', 'visitors', 'maintainers']

    for name in group_names:
        Group.objects.get_or_create(name=name)

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

def delete_db (): 
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

def init_db(): 
    
    create_user_groups()

    json_file_path = '../data/events_SpritzCollege.json'
    load_events_from_json(json_file_path)

    json_file_path = '../data/courses_SpritzCollege.json'
    load_courses_from_json(json_file_path)

