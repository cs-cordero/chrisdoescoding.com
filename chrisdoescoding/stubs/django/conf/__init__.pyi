from django.utils.functional import LazyObject

class LazySettings(LazyObject): ...

settings = LazySettings()
