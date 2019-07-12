from django.conf import settings
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed

from posts import models


class RssPostFeed(Feed):
    title = settings.TITLE
    link = "/"
    description = settings.DESCRIPTION

    def items(self) -> models.Post:
        return models.Post.objects.order_by("-publication_date")[:5]

    def item_title(self, item: models.Post) -> str:
        return item.title

    def item_description(self, item: models.Post) -> str:
        return item.excerpt

    def item_link(self, item: models.Post) -> str:
        return reverse("post", args=[item.pk])


class AtomPostFeed(RssPostFeed):
    feed_type = Atom1Feed
    subtitle = RssPostFeed.description
