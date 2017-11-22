from django.conf.urls import url
from django.contrib import admin

from .views import (
    post_list,
    post_detail,
    post_update,
    post_delete,
    post_create
    )

urlpatterns = [
    url(r'^$', post_list),
    url(r'^create/$', post_create),
    url(r'^(?P<id>\d+)/$', post_detail),
    url(r'^update/$', post_update),
    url(r'^delete/$', post_delete),
]
