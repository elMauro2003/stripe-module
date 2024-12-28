
from django.contrib import admin
from django.urls import path, include, re_path  # new]
from django.conf import settings
from django.views.static import serve


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("products.urls")),  # new
    re_path(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
