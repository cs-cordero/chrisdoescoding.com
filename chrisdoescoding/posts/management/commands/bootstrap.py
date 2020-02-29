from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.core.management.base import BaseCommand

import factories
from posts.models import Post


class Command(BaseCommand):
    help = (
        "Bootstrap the project with a single post and super user for admin. "
        "Creation only succeeds if there are no posts and if the "
        "'superuser' user does not exist."
    )

    def handle(self, *args, **options):
        if settings.DEBUG is False:
            raise ImproperlyConfigured(
                "Command bootstrap is not allowed in production environments!"
            )

        if not Post.objects.filter(publication_date__isnull=False).exists():
            factories.PostFactory()
        else:
            self.stdout.write(
                "A published post already exists, skipping published post creation.\n"
            )

        if not User.objects.filter(username="superuser").exists():
            call_command(
                "createsuperuser",
                "--noinput",
                username="superuser",
                email="superuser@test.com",
                stdout=self.stdout,
                stderr=self.stderr,
            )
            user = User.objects.get(username="superuser")
            user.set_password("test")
            user.save()
        else:
            self.stdout.write(
                "superuser already exists, skipping super user creation.\n"
            )
