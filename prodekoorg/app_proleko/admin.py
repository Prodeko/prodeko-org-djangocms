from django.contrib import admin

from .models import Post, Lehti


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "authors", "timestamp", "total_likes")


admin.site.register(Post, PostAdmin)
admin.site.register(Lehti)
