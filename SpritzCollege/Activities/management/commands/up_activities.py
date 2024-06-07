from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, datetime, time
import pytz
from Activities.models import Event, Course


class Command(BaseCommand):
    help = 'Load sample events and courses into the database'

    def handle(self, *args, **kwargs):

        rome_tz = pytz.timezone('Europe/Rome')

        Event.objects.all().delete()
        Course.objects.all().delete()

        # Event 2: Global Innovation Summit
        ev1 = Event.objects.create(
            name="Global Innovation Summit",
            date=datetime(year=2024, month=6, day=12, hour=8,
                          minute=31, tzinfo=rome_tz),
            place="conference room",
            description="The Global Innovation Summit is a premier event for professionals, entrepreneurs, and innovators from around the world. Held in the bustling city of Techville, this summit showcases the latest advancements in technology, business, and sustainability. Attendees can participate in keynote speeches, panel discussions, and networking sessions, making it a must-attend event for anyone looking to stay ahead in their field.",
            price=Decimal('15.60')
        )


        # Event 2: Modena Jazz Festival
        ev2 = Event.objects.create(
            name="Modena Jazz Festival",
            date=datetime(year=2024, month=6, day=25, hour=19,
                        minute=0, tzinfo=rome_tz),
            place="Piazza Grande, Modena",
            description="The Modena Jazz Festival is an annual event that brings together jazz enthusiasts from all over the world. Held in the historic Piazza Grande, the festival features performances by renowned jazz musicians, jam sessions, and workshops. Attendees can enjoy an evening filled with soulful music, delicious local food, and the charming ambiance of Modena.",
            price=Decimal('30.00')
        )

        # Event 3: Modena Food & Wine Fair
        ev3 = Event.objects.create(
            name="Modena Food & Wine Fair",
            date=datetime(year=2024, month=6, day=27, hour=11,
                        minute=0, tzinfo=rome_tz),
            place="Modena Exhibition Center",
            description="The Modena Food & Wine Fair is a celebration of the rich culinary heritage of Modena and the Emilia-Romagna region. Visitors can explore a variety of food stalls offering local delicacies, participate in wine tastings, and attend cooking demonstrations by top chefs. It's a perfect event for food lovers looking to experience the flavors and traditions of Modena.",
            price=Decimal('25.00')
        )
            
        # Event 4: Modena Art & Culture Festival
        ev4 = Event.objects.create(
            name="Modena Art & Culture Festival",
            date=datetime(year=2024, month=9, day=15, hour=10,
                        minute=0, tzinfo=rome_tz),
            place="Modena City Center",
            description="The Modena Art & Culture Festival is a vibrant celebration of the city's artistic heritage. This annual event features exhibitions from local and international artists, live performances, and interactive workshops. Visitors can immerse themselves in Modena's rich culture and enjoy a variety of art forms, including painting, sculpture, music, and dance.",
            price=Decimal('20.00')
        )

        # Event 5: Modena Technology Expo
        ev5 = Event.objects.create(
            name="Modena Technology Expo",
            date=datetime(year=2024, month=11, day=3, hour=9,
                        minute=0, tzinfo=rome_tz),
            place="Modena Expo Center",
            description="The Modena Technology Expo is an annual event showcasing the latest advancements in technology and innovation. This expo brings together tech enthusiasts, industry professionals, and leading companies to explore new products and trends. Attendees can participate in keynote sessions, product demonstrations, and networking opportunities, making it a must-attend event for anyone interested in technology.",
            price=Decimal('35.00')
        )
        
        self.stdout.write(self.style.SUCCESS(
            'All events have been successfully loaded'))
