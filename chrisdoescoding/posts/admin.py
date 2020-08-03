from django.contrib import admin

from posts.models import Post


class PostAdmin(admin.ModelAdmin):
    exclude = ("excerpt",)


admin.site.register(Post, PostAdmin)
