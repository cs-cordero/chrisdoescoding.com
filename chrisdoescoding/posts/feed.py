from django.conf import settings
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed

from posts import models


class RssPostFeed(Feed):
    title = settings.TITLE
    link = "/"
    description = settings.DESCRIPTION

    def items(self):
        return models.Post.objects.order_by("-publication_date")[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.excerpt

    def item_link(self, item):
        return reverse("post", args=[item.pk])


class AtomPostFeed(RssPostFeed):
    feed_type = Atom1Feed
    subtitle = RssPostFeed.description
