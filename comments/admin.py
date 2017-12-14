from django.contrib import admin

# Register your models here.
from .models import Comment

class CommentModelAdmin(admin.ModelAdmin):
    list_display = ["user", "content"]
    list_filter = ["timestamp"]
    search_fields = ["user", "content"]
    # exclude = ["photo_medium","photo_thumb"]

    class Meta:
        model = Comment
    

admin.site.register(Comment, CommentModelAdmin)
