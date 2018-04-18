from django.test import TestCase, RequestFactory
from django.utils import timezone

from chrisdoescoding.posts.models import Post
from chrisdoescoding.posts.views import BasePostView

from datetime import timedelta
from unittest.mock import patch

class FakeMarkdownParser:
    html = 'foo'

    def __exit__():
        pass

class TestView(TestCase):

    @classmethod
    def setUpTestData(cls):
        now = timezone.now()
        created = now - timedelta(hours=3)

        cls.post_0 = Post.objects.create(title='post 0',
                                         publication_date=now-timedelta(hours=2))
        cls.post_1 = Post.objects.create(title='post 1',
                                         publication_date=now-timedelta(hours=1))
        cls.post_2 = Post.objects.create(title='post 2')
        cls.post_3 = Post.objects.create(title='post 3',
                                         publication_date=now-timedelta(minutes=30),
                                         hide=True)
        cls.post_4 = Post.objects.create(title='post 4',
                                         publication_date=now-timedelta(hours=0))

    def test_unable_to_find_post(self):
        """ should 404 when user tries to look for a post that doesn't exist """
        response = self.client.get('/posts/100/', follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_unable_to_find_unpublished_post(self):
        """ should 404 when user tries to look for a post that isn't published """
        unpublished_post_id = self.post_2.id
        response = self.client.get(f'/posts/{unpublished_post_id}/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_unable_to_find_hidden_post(self):
        """ should 404 when user tries to look for a post that is hidden """
        hidden_post_id = self.post_3.id
        response = self.client.get(f'/posts/{hidden_post_id}/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_redirect_to_latest(self):
        """ homepage should redirect to latest post """
        response = self.client.get('/', follow=True)
        self.assertRedirects(response, '/posts/latest/')
        self.assertContains(response, self.post_4.title)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'single_post_view.html')

    def test_get_post_requested(self):
        """ posts should work as intended """
        published_posts = (self.post_0, self.post_1, self.post_4)
        for published_post in published_posts:
            response = self.client.get(f'/posts/{published_post.id}/')
            self.assertContains(response, published_post.title)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'single_post_view.html')

    @patch('chrisdoescoding.posts.views.MarkdownParser')
    def test_uses_markdownparser(self, mock_mp):
        """ posts should call the markdownparser """
        published_posts = (self.post_0, self.post_1, self.post_4)
        mock_mp.return_value.__enter__.return_value = FakeMarkdownParser
        for published_post in published_posts:
            response = self.client.get(f'/posts/{published_post.id}/')
            mock_mp.assert_called_with(published_post.body)
            self.assertContains(response, published_post.title)
            self.assertContains(response, FakeMarkdownParser.html)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'single_post_view.html')

    def test_sets_next_prev_ids_in_context(self):
        """ should accurately get the next or previous post """
        inputs_to_expected = (
            (self.post_0, (None, self.post_1.id)),
            (self.post_1, (self.post_0.id, self.post_4.id)),
            (self.post_4, (self.post_1.id, None))
        )

        for input_post, expected in inputs_to_expected:
            response = self.client.get(f'/posts/{input_post.id}/')
            context = response.context
            expected_prev, expected_next = expected
            actual_prev, actual_next = context['previous_post'], context['next_post']
            self.assertEqual(actual_prev, expected_prev)
            self.assertEqual(actual_next, expected_next)
