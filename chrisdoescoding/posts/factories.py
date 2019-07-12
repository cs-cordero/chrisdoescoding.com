from django.conf import settings
import dateutil
import factory

DEFAULT_TIMEZONE = dateutil.tz.gettz(settings.TIME_ZONE)


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "posts.Post"

    title = factory.Faker("sentence", nb_words=4)
    body = factory.Faker("text", max_nb_chars=200)
    created = factory.Faker("past_datetime", start_date="-30d", tzinfo=DEFAULT_TIMEZONE)
    hide = False

    @factory.post_generation
    def last_updated(obj, create, extracted, **kwargs):
        if not create:
            return
        obj.last_updated = (
            extracted
            or factory.Faker(
                "past_datetime", start_date=obj.created, tzinfo=DEFAULT_TIMEZONE
            ).generate()
        )

    @factory.post_generation
    def publication_date(obj, create, extracted, **kwargs):
        if not create:
            return
        obj.publication_date = (
            extracted
            or factory.Faker(
                "past_datetime", start_date=obj.created, tzinfo=DEFAULT_TIMEZONE
            ).generate()
        )


PublishedPostFactory = PostFactory


class UnpublishedPostFactory(PostFactory):
    publication_date = None
