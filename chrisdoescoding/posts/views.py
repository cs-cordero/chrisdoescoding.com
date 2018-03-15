from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.http import HttpResponseRedirect

from chrisdoescoding.posts.models import Post
from chrisdoescoding.posts.utils import MarkdownParser

from datetime import datetime


class BasePostView(DetailView):
    model = Post
    queryset = Post.objects.filter(publication_date__lte=datetime.utcnow())

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object:
            raise Http404('Did not find a published post to return!')
        context = self.get_context_data(object=self.object)
        with MarkdownParser(self.object.body) as markdown:
            context.update({ 'markdown': markdown })
        return self.render_to_response(context)


class LatestPostView(BasePostView):
    template_name = 'latest_post_view.html'

    def get_object(self):
        return self.get_queryset().latest('publication_date')


class PostView(BasePostView):
    template_name = 'single_post_view.html'


class AllPostsView(ListView):
    template_name = 'all_posts_view.html'
    context_object_name = 'published_posts'
    queryset = Post.objects.filter(publication_date__lte=datetime.utcnow())
