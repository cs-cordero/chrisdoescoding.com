from datetime import timedelta
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from posts.models import Post, calculate_excerpt_from_markdown


class FakeMarkdownParser:
    html = "foo"

    def __exit__(self):
        pass


class TestView(TestCase):
    @classmethod
    def setUpTestData(cls):
        now = timezone.now()

        cls.post_0 = Post.objects.create(
            title="post 0",
            publication_date=now - timedelta(hours=2),
            body="# Hello this is post_0!\nHello",
        )
        cls.post_1 = Post.objects.create(
            title="post 1",
            publication_date=now - timedelta(hours=1),
            body="# Hello this is post_1!\nHello",
        )
        cls.post_2 = Post.objects.create(title="post 2")
        cls.post_3 = Post.objects.create(
            title="post 3",
            publication_date=now - timedelta(minutes=30),
            body="# Hello this is post_3!\nHello",
            hide=True,
        )
        cls.post_4 = Post.objects.create(
            title="post 4",
            publication_date=now - timedelta(hours=0),
            body="# Hello this is post_4!\nHello",
        )

    def test_unable_to_find_post(self):
        """ should 404 when user tries to look for a post that doesn't exist """
        url = reverse("post", args=[100])
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")

    def test_unable_to_find_unpublished_post(self):
        """ should 404 when user tries to look for a post that isn't published """
        unpublished_post_id = self.post_2.id
        url = reverse("post", args=[unpublished_post_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")

    def test_unable_to_find_hidden_post(self):
        """ should 404 when user tries to look for a post that is hidden """
        hidden_post_id = self.post_3.id
        url = reverse("post", args=[hidden_post_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")

    def test_redirect_to_latest(self):
        """ homepage should redirect to latest post """
        url = reverse("home")
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, reverse("latest"))
        self.assertContains(response, self.post_4.title)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "detail_view.html")

    def test_get_post_requested(self):
        """ posts should work as intended """
        published_posts = (self.post_0, self.post_1, self.post_4)
        for published_post in published_posts:
            url = reverse("post", args=[published_post.id])
            response = self.client.get(url)
            self.assertContains(response, published_post.title)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "detail_view.html")

    @patch("posts.views.MarkdownParser")
    def test_uses_markdownparser(self, mock_mp):
        """ posts should call the markdownparser """
        published_posts = (self.post_0, self.post_1, self.post_4)
        mock_mp.return_value.__enter__.return_value = FakeMarkdownParser
        for published_post in published_posts:
            url = reverse("post", args=[published_post.id])
            response = self.client.get(url)
            mock_mp.assert_called_with(published_post.body)
            self.assertContains(response, published_post.title)
            self.assertContains(response, FakeMarkdownParser.html)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "detail_view.html")

    def test_sets_next_prev_ids_in_context(self):
        """ should accurately get the next or previous post """
        inputs_to_expected = (
            (self.post_0, (None, self.post_1.id)),
            (self.post_1, (self.post_0.id, self.post_4.id)),
            (self.post_4, (self.post_1.id, None)),
        )

        for input_post, expected in inputs_to_expected:
            url = reverse("post", args=[input_post.id])
            response = self.client.get(url)
            context = response.context
            expected_prev, expected_next = expected
            actual_prev, actual_next = context["previous_post"], context["next_post"]
            self.assertEqual(
                actual_prev.pk if actual_prev else actual_prev, expected_prev
            )
            self.assertEqual(
                actual_next.pk if actual_next else actual_next, expected_next
            )

    @patch("posts.views.MarkdownParser")
    def test_raw_returns_post_body(self, mock_mp):
        """ detailview posts with raw param should return the text body """
        published_posts = (self.post_0, self.post_1, self.post_4)
        mock_mp.return_value.__enter__.return_value = FakeMarkdownParser
        for published_post in published_posts:
            url = f'{reverse("post", args=[published_post.id])}?raw'
            response = self.client.get(url)
            mock_mp.assert_not_called()
            self.assertContains(response, published_post.body)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response["content-type"], "text/plain")

    def test_excerpt_calculation(self):
        assert calculate_excerpt_from_markdown(self.post_4.body) == self.post_4.excerpt
        assert (
            calculate_excerpt_from_markdown("[Google](https://google.com)") == "Google"
        )
