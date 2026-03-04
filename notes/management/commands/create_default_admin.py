"""
Management command to create default admin user
Run with: python manage.py create_default_admin
Supports environment variables for custom credentials
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = 'Creates a default admin user if it does not exist'

    def handle(self, *args, **kwargs):
        # Get credentials from environment variables or use defaults
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        email = os.environ.get('ADMIN_EMAIL', 'admin@notesplatform.com')
        password = os.environ.get('ADMIN_PASSWORD', 'admin123')

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
                    f'\n  Email: {email}'
                    f'\n  Password: {"*" * len(password)} (check environment variable or default: admin123)'
                    f'\n  ⚠️  Remember to change the password after first login!\n'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'Admin user "{username}" already exists. Skipping...'
                )
            )
