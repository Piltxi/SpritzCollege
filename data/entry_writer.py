import json
import random
from faker import Faker

def courses (quantity):
    fake = Faker()
    course_list = []
    for _ in range(quantity):
        name = fake.catch_phrase()
        description = fake.text()
        start_date = fake.date_time_between(start_date='-30d', end_date='+30d', tzinfo=None)
        end_date = fake.date_time_between(start_date=start_date, end_date='+60d', tzinfo=None)
        recurrence_day = fake.random_element(elements=('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'))
        
        course = {
            'name': name,
            'description': description,
            'start_date': start_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'end_date': end_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'recurrence_day': recurrence_day
        }
        course_list.append(course)
    
    return course_list
    
def events(quantity):
    fake = Faker()
    
    event_list = []
    
    for _ in range(quantity):
        name = fake.name() + " Event"
        description = fake.text()
        date = fake.date_time_between(start_date='-30d', end_date='+30d').isoformat()
        price = round(random.uniform(0.0, 100.0), 2) if random.choice([True, False]) else None

        event = {
            'name': name,
            'description': description,
            'date': date,
            'price': price
        }
        event_list.append(event)
    
    return event_list

def main():
    
    quantity = 100
    out_file = "events_SpritzCollege.json"
    events_data = events(quantity)
    
    with open(out_file, 'w') as f:
        json.dump(events_data, f, indent=4)

    quantity = 10
    out_file = "courses_SpritzCollege.json"
    courses_data = courses (quantity)
    
    with open(out_file, 'w') as f:
        json.dump(courses_data, f, indent=4)

if __name__ == "__main__":
    main()
