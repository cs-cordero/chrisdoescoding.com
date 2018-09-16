from django.conf import settings
from django.db import models

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
        # TODO: Check if this works when the body is filled with markdown...
        # it probably won't :(
        excerpt_length = settings.LISTVIEW_EXCERPT_LENGTH
        return (
            f'{self.body[:excerpt_length]}...'
            if len(self.body) > excerpt_length else self.body
        )
