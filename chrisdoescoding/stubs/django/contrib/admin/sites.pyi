from django.utils.functional import LazyObject

class DefaultAdminSite(LazyObject):
    def _setup(self): ...

    # hardcoded for ease-of-typing
    def register(self, model_or_iterable, admin_class=None, **options): ...

site = DefaultAdminSite()
