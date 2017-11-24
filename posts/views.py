from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .forms import PostForm
from .models import Post
#cоздание поста
def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instanse = form.save(commit=False)
        instanse.save()
        messages.success(request, "Успешно создан")
        return HttpResponseRedirect(instanse.get_absolut_url())
    context = {
        "form":form
    }

    return render(request, "post_form.html", context)

#просмотр поста
def post_detail(request, id=None):
    instance = get_object_or_404(Post, id=id)
    context = {       
       "instance": instance  
    }
    return render(request, "post_detail.html", context)

#список постов
def post_list(request):
    queryset_list = Post.objects.all()

    paginator = Paginator(queryset_list, 3) # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    # Get the index of the current page
    index = queryset.number - 1  # edited to something easier without index 
    # This value is maximum index of your pages, so the last page - 1
    max_index = len(paginator.page_range)  
    # You want a range of 7, so lets calculate where to slice the list
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    # Get our new page range. In the latest versions of Django page_range returns 
    # an iterator. Thus pass it to list, to make our slice possible again.
    page_range = list(paginator.page_range)[start_index:end_index] 

    context = {
        "object_list": queryset,
        "title": "List",
        "page_request_var":page_request_var,
        "page_range":page_range
    }
    return render(request, "post_list.html", context)

#обновление поста
def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instanse = form.save(commit=False)
        instanse.save()       
        messages.success(request, "Успешно Обновлен", extra_tags='some-tag')
        return HttpResponseRedirect(instanse.get_absolut_url())
    context = {       
       "instance": instance,
       "form":form  
    }
    return render(request, "post_form.html", context)

#удаление поста
def post_delete(request, id=None):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "Успешно Удален")
    return redirect("posts:list")
