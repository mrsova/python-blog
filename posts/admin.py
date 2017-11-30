from django.contrib import admin
# Register your models here.
from .models import Post


class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "updated", "timestamp"]
    list_filter = ["updated", "timestamp"]
    search_fields = ["title", "content"]
    # exclude = ["photo_medium","photo_thumb"]

    class Meta:
        model = Post
    

admin.site.register(Post, PostModelAdmin)
