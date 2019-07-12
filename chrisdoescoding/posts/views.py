import random
from typing import Any, Dict, Optional

from django.http import Http404, HttpRequest, HttpResponse
from django.utils import timezone
from django.views.generic import DetailView, ListView, RedirectView

from posts.models import Post
from posts.utils import MarkdownParser


class BasePostView(DetailView):
    object: Post
    model = Post

    def get_queryset(self):
        self.queryset = Post.objects.filter(
            publication_date__lte=timezone.now()
        ).filter(hide=False)
        return self.queryset

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        # find the post
        self.object = self.get_object()  # type: ignore
        if not self.object:
            raise Http404("Did not find a published post to return!")

        if "raw" in request.GET:
            return HttpResponse(
                self.object.body, content_type="text/plain"  # type: ignore
            )

        # build the context
        context = self.get_context_data(object=self.object)
        with MarkdownParser(self.object.body) as markdown:  # type: ignore
            context.update({"markdown": markdown})
        context.update(self.get_next_and_prev(self.object))

        return self.render_to_response(context)

    def get_next_and_prev(self, current: Post) -> Dict[str, Optional[Post]]:
        reference_time = current.publication_date
        published_posts = self.get_queryset()

        previous_post: Optional[Post]
        next_post: Optional[Post]
        try:
            previous_post = published_posts.filter(
                publication_date__lt=reference_time
            ).latest("publication_date")
        except Post.DoesNotExist:
            previous_post = None
        try:
            next_post = published_posts.filter(
                publication_date__gt=reference_time
            ).earliest("publication_date")
        except Post.DoesNotExist:
            next_post = None

        return {"previous_post": previous_post, "next_post": next_post}


class LatestPostView(BasePostView):
    template_name = "detail_view.html"

    def get_object(self) -> Optional[Post]:  # type: ignore
        try:
            return self.get_queryset().latest("publication_date")  # type: ignore
        except Post.DoesNotExist:
            return None


class PostView(BasePostView):
    template_name = "detail_view.html"


class AllPostsView(ListView):
    template_name = "list_view.html"
    context_object_name = "published_posts"

    def get_queryset(self):
        self.queryset = (
            Post.objects.filter(publication_date__lte=timezone.now())
            .filter(hide=False)
            .order_by("-publication_date")
        )
        return self.queryset


class RandomPostView(RedirectView):
    def get_queryset(self):
        self.queryset = Post.objects.filter(
            publication_date__lte=timezone.now()
        ).filter(hide=False)
        return self.queryset

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str:
        published_posts = self.get_queryset()
        random_selection = random.randint(0, len(published_posts) - 1)
        post_id = published_posts[random_selection].id
        return f"/posts/{post_id}"
