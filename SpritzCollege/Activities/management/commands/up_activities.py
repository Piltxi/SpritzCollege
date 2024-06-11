from decimal import Decimal
from django.core.management.base import BaseCommand
from datetime import date, datetime, time
import pytz
from Activities.models import Course, Event


class Command(BaseCommand):
    help = 'Load some events and courses into the database'

    def handle(self, *args, **kwargs):
        rome_tz = pytz.timezone('Europe/Rome')

        Event.objects.all().delete()
        Course.objects.all().delete()

        Event.objects.create(
            name="Web Technologies Exam",
            date=rome_tz.localize(datetime(2024, 6, 12, 9, 41)),
            price=Decimal('0.00'),
            description="Exam to verify skills for web technologies and the django framework.",
            place="University - Capodieci Office"
        )
        
        Event.objects.create(
            name="Languages Compilers Exam",
            date=rome_tz.localize(datetime(2024, 6, 25, 9, 41)),
            price=Decimal('0.00'),
            description="Exam to verify skills for Languages and Compilers LLVM framework.",
            place="University - FIM"
        )
        
        Event.objects.create(
            name="Languages Compilers Exam",
            date=rome_tz.localize(datetime(2024, 6, 27, 9, 41)),
            price=Decimal('0.00'),
            description="Exam to verify skills Compilers LLVM framework.",
            place="University - FIM"
        )

        Event.objects.create(
            name="Motor Valley Fest 2025",
            date=rome_tz.localize(datetime(2025, 5, 2, 10, 0)),
            price=Decimal('0.00'),
            description="An open-air festival celebrating Italian motoring history and excellence.",
            place="Modena"
        )

        Event.objects.create(
            name="Festival Filosofia",
            date=rome_tz.localize(datetime(2024, 9, 13, 9, 0)),
            price=Decimal('0.00'),
            description="A philosophical festival with the theme 'Psyche'.",
            place="Modena"
        )
        Event.objects.create(
            name="Emilia Food Fest",
            date=rome_tz.localize(datetime(2024, 9, 20, 10, 0)),
            price=Decimal('0.00'),
            description="A festival dedicated to the flavors and traditions of Via Emilia.",
            place="Carpi"
        )
        Event.objects.create(
            name="Modena Cento Ore",
            date=rome_tz.localize(datetime(2024, 10, 6, 8, 0)),
            price=Decimal('0.00'),
            description="A classic car rally with scenic drives and gourmet experiences.",
            place="Modena"
        )
        Event.objects.create(
            name="Festa della Musica",
            date=rome_tz.localize(datetime(2024, 6, 21, 18, 0)),
            price=Decimal('38.62'),
            description="A music festival featuring performances by New Candys and Ditz (UK).",
            place="Modena"
        )
        Event.objects.create(
            name="Arti Vive Festival",
            date=rome_tz.localize(datetime(2024, 7, 4, 17, 0)),
            price=Decimal('32.09'),
            description="A cultural festival with music, art installations, and performances.",
            place="Soliera"
        )
        Event.objects.create(
            name="Villa Summer Festival",
            date=rome_tz.localize(datetime(2024, 7, 12, 18, 0)),
            price=Decimal('22.78'),
            description="A summer music festival featuring Rudeejay.",
            place="Modena"
        )
        Event.objects.create(
            name="Pignoletto Fest Warm Up",
            date=rome_tz.localize(datetime(2024, 8, 14, 20, 0)),
            price=Decimal('23.28'),
            description="A music festival featuring Hellripper.",
            place="Modena"
        )
        Event.objects.create(
            name="KEFestival",
            date=rome_tz.localize(datetime(2024, 9, 7, 19, 0)),
            price=Decimal('29.25'),
            description="A music festival featuring Cyberpunkers and NASKA.",
            place="Modena"
        )
        Event.objects.create(
            name="Fiorella Mannoia Concert",
            date=rome_tz.localize(datetime(2024, 7, 17, 21, 0)),
            price=Decimal('27.89'),
            description="A concert by Fiorella Mannoia.",
            place="Piazza Roma, Modena"
        )
        Event.objects.create(
            name="University Open Day",
            date=rome_tz.localize(datetime(2025, 3, 15, 9, 0)),
            price=Decimal('0.00'),
            description="Open day for prospective students to explore programs and campus.",
            place="University of Modena and Reggio Emilia"
        )
        Event.objects.create(
            name="Research Symposium",
            date=rome_tz.localize(datetime(2025, 4, 10, 9, 0)),
            price=Decimal('0.00'),
            description="Symposium showcasing the latest research from various departments.",
            place="University of Modena and Reggio Emilia"
        )
        Event.objects.create(
            name="Career Fair",
            date=rome_tz.localize(datetime(2025, 5, 5, 10, 0)),
            price=Decimal('0.00'),
            description="Connecting students with potential employers from various industries.",
            place="University of Modena and Reggio Emilia"
        )
        Event.objects.create(
            name="Alumni Networking Event",
            date=rome_tz.localize(datetime(2024, 6, 20, 18, 0)),
            price=Decimal('0.00'),
            description="Event for alumni to reconnect and network with current students and faculty.",
            place="University of Modena and Reggio Emilia"
        )
        Event.objects.create(
            name="International Student Orientation",
            date=rome_tz.localize(datetime(2024, 9, 1, 9, 0)),
            price=Decimal('0.00'),
            description="Orientation for incoming international students.",
            place="University of Modena and Reggio Emilia"
        )
        Event.objects.create(
            name="Engineering Expo",
            date=rome_tz.localize(datetime(2024, 10, 8, 9, 0)),
            price=Decimal('0.00'),
            description="Expo featuring projects and innovations from the engineering faculty.",
            place="University of Modena and Reggio Emilia"
        )
        Event.objects.create(
            name="Sustainability Conference",
            date=rome_tz.localize(datetime(2024, 11, 3, 9, 0)),
            price=Decimal('0.00'),
            description="Conference focusing on sustainability practices and research.",
            place="University of Modena and Reggio Emilia"
        )
        Event.objects.create(
            name="Student Art Exhibition",
            date=rome_tz.localize(datetime(2025, 2, 14, 9, 0)),
            price=Decimal('0.00'),
            description="Exhibition showcasing artwork by university students.",
            place="University of Modena and Reggio Emilia"
        )
        Event.objects.create(
            name="Hackathon",
            date=rome_tz.localize(datetime(2025, 4, 25, 10, 0)),
            price=Decimal('0.00'),
            description="24-hour hackathon where students develop innovative solutions.",
            place="University of Modena and Reggio Emilia"
        )
        Event.objects.create(
            name="Cultural Diversity Week",
            date=rome_tz.localize(datetime(2025, 5, 22, 9, 0)),
            price=Decimal('0.00'),
            description="Week-long celebration of cultural diversity with various events.",
            place="University of Modena and Reggio Emilia"
        )
        Event.objects.create(
            name="Health and Wellness Fair",
            date=rome_tz.localize(datetime(2025, 3, 7, 9, 0)),
            price=Decimal('0.00'),
            description="Event promoting health and wellness among students.",
            place="University of Modena and Reggio Emilia"
        )
        Event.objects.create(
            name="Literary Festival",
            date=rome_tz.localize(datetime(2024, 10, 18, 9, 0)),
            price=Decimal('0.00'),
            description="Festival celebrating literature with author readings and discussions.",
            place="University of Modena and Reggio Emilia"
        )
        Event.objects.create(
            name="Science Day",
            date=rome_tz.localize(datetime(2024, 11, 14, 9, 0)),
            price=Decimal('0.00'),
            description="Day dedicated to science demonstrations and lectures.",
            place="University of Modena and Reggio Emilia"
        )
        Event.objects.create(
            name="TEDxModena",
            date=rome_tz.localize(datetime(2025, 4, 17, 9, 0)),
            price=Decimal('0.00'),
            description="TEDx event featuring talks by local thinkers and innovators.",
            place="University of Modena and Reggio Emilia"
        )
        Event.objects.create(
            name="Music and Arts Festival",
            date=rome_tz.localize(datetime(2025, 6, 10, 9, 0)),
            price=Decimal('0.00'),
            description="Festival showcasing musical and artistic talents of students.",
            place="University of Modena and Reggio Emilia"
        )
        
        Course.objects.create(
            name="Data Structures",
            start_date=date(2024, 9, 2),
            end_date=date(2024, 12, 16),
            recurrence_day="Tuesday",
            description="Study of data structures such as arrays, stacks, queues, linked lists, trees, and graphs.",
            time= time(11, 0),
            category= "TCH",
        )
        
        Course.objects.create(
            name="Software Engineering",
            start_date=date(2024, 9, 5),
            end_date=date(2024, 12, 19),
            recurrence_day="Friday",
            description="Principles of software engineering including software development lifecycle, agile methodologies, and project management.",
            time=time(10, 0),
            category= "TCH",
        )
        
        Course.objects.create(
            name="Computer Networks",
            start_date=date(2024, 9, 10),
            end_date=date(2024, 12, 24),
            recurrence_day="Wednesday",
            description="Introduction to computer networks, network protocols, and internet architecture.",
            time=time(11, 0),
            category= "TCH",
        )
        
        self.stdout.write(self.style.SUCCESS(
            'All activities have been successfully loaded'))
