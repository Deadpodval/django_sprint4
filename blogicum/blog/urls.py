from django.urls import path

from .views import (
    PostListView,
    PostCreateView,
    PostCategoryView,
    PostDetailView,
    PostUpdateView,
    CommentCreateView,
    CommentUpdateView,
    UserDetailView,
)

app_name = 'blog'


urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('create/', PostCreateView.as_view(), name='create_post'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:category_slug>/',
         PostCategoryView.as_view(), name='category_posts'),
    path('posts/<int:pk>/edit', PostUpdateView.as_view(), name='post_edit'),
    path('posts/<post_id>/comment/', CommentCreateView.as_view(), name='comment_edit'),
    path('posts/<post_id>/edit_comment/<comment_id>/', CommentUpdateView.as_view(), name='comment_edit'),
    path('profile/<user_id>/', UserDetailView.as_view(), name='profile'),
]
