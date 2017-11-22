from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Post

def post_create(request):
    context = {
       "title": "Create" 
    }

    return render(request, "index.html", context)

def post_detail(request, id=None):
    #instance = Post.objects.get(id=10)
    instance = get_object_or_404(Post, id=id)
    context = {       
       "instance": instance  
    }

    return render(request, "post_detail.html", context)

def post_list(request):
    queryset = Post.objects.all()
    context = {
        "object_list": queryset,
        "title": "List" 
    }
    # if request.user.is_authenticated():    
    #     context = {
    #        "title": "my user List" 
    #     }
    # else:
    #      context = {
    #        "title": "List" 
    #     }
    return render(request, "index.html", context)

def post_update(request):
    context = {
        "title": "Update" 
    }

    return render(request, "index.html", context)

def post_delete(request):
    context = {
        "title": "Delete" 
    }
    
    return render(request, "index.html", context)
