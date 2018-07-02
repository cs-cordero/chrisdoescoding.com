from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

import json
import random

class SouthParkView(TemplateView):
    template_name = 'southpark.html'


class SouthParkRedirectView(RedirectView):
    permanent = False
    query_string = False

    with open('chrisdoescoding/southpark/scripts/southpark.json', 'r') as f:
        data = json.loads(f.read())

    south_park_ids = list({episode.get('id') for episode in data})

    def get_redirect_url(self, *args, **kwargs):
        count_ids = len(self.south_park_ids)
        sp_id = self.south_park_ids[random.randint(0, count_ids+1)]
        return f'https://hulu.com/watch/{sp_id}'
