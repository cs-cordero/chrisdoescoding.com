from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.http import HttpResponseRedirect

from chrisdoescoding.posts.models import Post
from chrisdoescoding.posts.utils import MarkdownParser

import datetime


class PostView(DetailView):
    model = Post
    template_name = 'postview.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.publication_date:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

        return HttpResponseRedirect('/posts')


class LatestPostView(DetailView):
    model = Post
    template_name = 'postview.html'

    def get(self, request):
        now = datetime.datetime.utcnow()
        self.object = Post.objects.filter(publication_date__lte=now) \
                                  .order_by('-publication_date')[0]
        #TODO: Handle case where no object is returned
        context = self.get_context_data(object=self.object)
        with MarkdownParser(self.object.body) as markdown:
            context.update({ 'markdown': markdown })
        return self.render_to_response(context)


class AllPostsView(ListView):
    template_name = 'listview.html'
    context_object_name = 'published_posts'

    def get_queryset(self):
        now = datetime.datetime.now()
        return Post.objects.filter(publication_date__lte=now)
