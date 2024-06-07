from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = 'Load sample users into the database'

    def handle(self, *args, **kwargs):

        # Create groups if they don't exist
        group_names = ['administration', 'culture', 'visitors']
        groups = {}
        for name in group_names:
            group, created = Group.objects.get_or_create(name=name)
            groups[name] = group
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created group: {name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Group {name} already exists'))
        
        self.stdout.write(self.style.SUCCESS("-> Created user groups"))

        # Define users and their group assignments
        users = [
            {'username': 'elia', 'password': 'pitz', 'group': 'all'},
            {'username': 'visitor1', 'password': 'tecnologieweb', 'group': 'visitors'},
            {'username': 'visitor2', 'password': 'tecnologieweb', 'group': 'visitors'},
            {'username': 'Nicola', 'password': 'capodieci', 'group': 'culture'},
            {'username': 'Claudia', 'password': 'django-channels', 'group': 'administration'},
        ]

        for user_data in users:
            username = user_data['username']
            password = user_data['password']
            group_name = user_data['group']

            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f'User {username} already exists, skipped.'))
                continue

            user = User.objects.create_user(username=username, password=password)
            self.stdout.write(self.style.SUCCESS(f'Created user: {username}'))

            if group_name == 'all':
                for group in groups.values():
                    user.groups.add(group)
                self.stdout.write(self.style.SUCCESS(f'Assigned user {username} to all groups'))
            elif group_name in groups:
                user.groups.add(groups[group_name])
                self.stdout.write(self.style.SUCCESS(f'Assigned user {username} to group {group_name}'))

        self.stdout.write(self.style.SUCCESS('All users have been successfully loaded'))
