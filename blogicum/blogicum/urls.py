from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('blog.urls', namespace='blog')),

    path('pages/', include('pages.urls', namespace='pages')),

    path('auth/', include('users.urls', namespace='users')),

    path('admin/', admin.site.urls),

    path('', include('django.contrib.auth.urls')),
]
