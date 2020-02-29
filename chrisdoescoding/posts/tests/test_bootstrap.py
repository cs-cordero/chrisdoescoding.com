import os
from unittest.mock import MagicMock

from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.test import TestCase, override_settings

import factories
from posts.models import Post


@override_settings(DEBUG=True)
class TestBootstrap(TestCase):
    def setUp(self):
        self.devnull = open(os.devnull, "w")

    def tearDown(self):
        self.devnull.close()
        self.devnull = None

    @override_settings(DEBUG=False)
    def test_command_fails_in_prod(self):
        with self.assertRaises(ImproperlyConfigured):
            call_command("bootstrap", stdout=self.devnull)

    def test_creates_post_when_it_doesnt_exist_before(self):
        assert Post.objects.count() == 0
        call_command("bootstrap", stdout=self.devnull)
        assert Post.objects.count() == 1

    def test_creates_published_post_if_only_unpublished_posts_exist(self):
        factories.UnpublishedPostFactory()
        assert Post.objects.count() == 1
        call_command("bootstrap", stdout=self.devnull)
        assert Post.objects.count() == 2

    def test_creates_superuser_when_it_doesnt_exist_before(self):
        assert not User.objects.filter(username="superuser").exists()
        call_command("bootstrap", stdout=self.devnull)
        assert User.objects.filter(username="superuser").exists()
        call_command("bootstrap", stdout=self.devnull)
        assert User.objects.filter(username="superuser").count() == 1

    def test_sets_superuser_password_to_test(self):
        call_command("bootstrap", stdout=self.devnull)
        user = User.objects.get(username="superuser")
        assert user.check_password("test")

    def test_command_uses_correct_stdout(self):
        spy = MagicMock()
        call_command("bootstrap", stdout=spy)
        spy.write.assert_called_once_with("Superuser created successfully.\n")
        spy.write.reset_mock()

        call_command("bootstrap", stdout=spy)
        assert spy.write.call_count == 2
        spy.write.assert_any_call(
            "A published post already exists, skipping published post creation.\n"
        )
        spy.write.assert_any_call(
            "superuser already exists, skipping super user creation.\n"
        )
