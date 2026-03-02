"""
Management command to create default admin user
Run with: python manage.py create_default_admin
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Creates a default admin user if it does not exist'

    def handle(self, *args, **kwargs):
        username = 'admin'
        email = 'admin@notesplatform.com'
        password = 'admin123'
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'\nDefault admin created successfully!'
                    f'\n  Username: {username}'
                    f'\n  Password: {password}'
                    f'\n  Remember to change the password in production!\n'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'Admin user "{username}" already exists.'
                )
            )
