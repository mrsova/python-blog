from django.shortcuts import render, get_object_or_404

from .models import Comment
# Create your views here.
def comment_thread(request, id):
    obj = get_object_or_404(Comment, id=id)
    context = {
        "comment": obj,
    }
    return render(request, "comment_thread.html",context)
