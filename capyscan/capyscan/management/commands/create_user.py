from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create a user'

    def handle(self, *args, **kwargs):
        username = 'Capymaster'
        password = 'capymaster'
        email = 'admin@capybara.page'

        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username, email, password)
            self.stdout.write(self.style.SUCCESS(f'User {username} created successfully!'))
        else:
            self.stdout.write(self.style.SUCCESS(f'User {username} already exists.'))
