from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),
    path('', include('app.urls',)), 
    path("api/", include("rest_framework.urls", namespace="rest_framework")),
]
