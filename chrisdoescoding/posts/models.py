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
