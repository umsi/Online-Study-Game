import os

from django.core.management.base import BaseCommand

from ...models import GamesUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        admin_username = os.environ.get("ADMIN_USERNAME")
        admin_password = os.environ.get("ADMIN_PASSWORD")

        if not GamesUser.objects.filter(username=admin_username).exists():
            GamesUser.objects.create_superuser(admin_username, "", admin_password)
