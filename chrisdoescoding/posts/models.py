from django.conf import settings
from django.db import models

from . import utils

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    publication_date = models.DateTimeField(auto_now=False, null=True, blank=True)
    hide = models.BooleanField(default=False)

    def __str__(self):
        prefix = ('(DRAFT {})'.format(self.last_updated.strftime('%m/%d/%Y'))
                  if not self.publication_date else '')
        return '{} {}'.format(prefix, self.title)

    @property
    def excerpt(self):
        excerpt_length = settings.LISTVIEW_EXCERPT_LENGTH

        markdown_body = utils.MarkdownParser(self.body).html
        first_p_tag_open = markdown_body.find('<p>')
        first_p_tag_close = markdown_body.find('</p>')

        if first_p_tag_open >= 0 and first_p_tag_close >= 0:
            excerpt = markdown_body[first_p_tag_open+3:first_p_tag_close]
            return (
                f'{excerpt[:excerpt_length]}...'
                if len(excerpt) > excerpt_length
                else excerpt
            )
        return ''
