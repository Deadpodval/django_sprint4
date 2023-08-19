from django.urls import path, include

from .views import PostListView, PostCreateView, PostCategoryView, PostDetailView


app_name = 'blog'

urlpatterns = [
    path('', PostCreateView.as_view(), name='create'),
    path('', PostListView.as_view(), name='index'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:category_slug>/',
         PostCategoryView.as_view(), name='category_posts'),
]
