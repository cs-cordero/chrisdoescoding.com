from django.shortcuts import render
from django.views.generic import DetailView
from django.http import HttpResponseRedirect

from chrisdoescoding.posts.models import Post


class PostView(DetailView):
    model = Post
    template_name = 'postview.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.publication_date:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

        return HttpResponseRedirect('/posts')
