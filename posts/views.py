from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
# Create your views here.
from comments.forms import CommentForm
from comments.models import Comment
from .forms import PostForm
from .models import Post
#cоздание поста
def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if not request.user.is_authenticated():
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instanse = form.save(commit=False)
        instanse.user = request.user
        instanse.save()
        messages.success(request, "Успешно создан")
        return HttpResponseRedirect(instanse.get_absolut_url())
    context = {
        "form":form
    }

    return render(request, "post_form.html", context)

#просмотр поста
def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    #Связка по ключу
    
    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        new_comment, created = Comment.objects.get_or_create(
                                  user = request.user,
                                  content_type=content_type,
                                  object_id=obj_id,
                                  content=content_data
                            )

    comments = Comment.objects.filter_by_instance(instance)
    #########################
    #Post.object.get(id=instance.id)
    context = {       
       "instance": instance,
       "comments": comments,
       "comment_form": form  
    }
    return render(request, "post_detail.html", context)

#список постов
def post_list(request):
    queryset_list = Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()

    query = request.GET.get("q")
    if query:
      queryset_list = queryset_list.filter(
              Q(title__icontains=query) |
              Q(content__icontains=query) |
              Q(user__first_name__icontains=query) |
              Q(user__last_name__icontains=query)
              ).distinct()

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
        "page_request_var": page_request_var,
        "page_range": page_range
    }
    return render(request, "post_list.html", context)

#обновление поста
def post_update(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if not request.user.is_authenticated():
        raise Http404
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
    if not request.user.is_staff or not request.user.superuser:
        raise Http404
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "Успешно Удален")
    return redirect("posts:list")
