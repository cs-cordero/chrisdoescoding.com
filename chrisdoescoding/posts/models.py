from bs4 import BeautifulSoup
from django.conf import settings
from django.db import models

from posts import utils


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    body = models.TextField()
    excerpt = models.CharField(max_length=settings.LISTVIEW_EXCERPT_LENGTH)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    publication_date = models.DateTimeField(auto_now=False, null=True, blank=True)
    hide = models.BooleanField(default=False)

    def __str__(self) -> str:
        prefix = (
            "(DRAFT {})".format(self.last_updated.strftime("%m/%d/%Y"))
            if not self.publication_date
            else ""
        )
        return "{} {}".format(prefix, self.title)

    def save(self, *args, **kwargs) -> None:
        self.excerpt = calculate_excerpt_from_markdown(self.body)
        super().save(*args, **kwargs)


def calculate_excerpt_from_markdown(markdown: str) -> str:
    excerpt_length = settings.LISTVIEW_EXCERPT_LENGTH

    markdown_body: str = utils.MarkdownParser(markdown).html
    soup_text: str = BeautifulSoup(markdown_body, "html.parser").text

    if len(soup_text) > excerpt_length:
        return f"{soup_text[:excerpt_length-3]}..."
    else:
        return soup_text
