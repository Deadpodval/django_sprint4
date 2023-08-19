from datetime import datetime

from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Category, Post
from django.views.generic import CreateView, ListView, DetailView


POSTS_PAGINATION = 5
POSTS_ORDERING = 'pub_date'
PAGINATOR_CATEGORY = 5


class PostListView(ListView):
    template_name = 'blog/index.html'
    model = Post
    ordering: str = POSTS_ORDERING
    paginate_by = POSTS_PAGINATION
    queryset = Post.objects.select_related(
        'location',
        'category').filter(is_published=True,
                           category__is_published=True,
                           pub_date__lte=datetime.now()
                           )


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, id=self.kwargs['pk'])
        return context


class PostCreateView(CreateView, LoginRequiredMixin):
    model = Post
    fields = [
        'title',
        'text',
        'location',
        'category',
    ]
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')


class PostCategoryView(ListView):
    model = Post
    template_name = 'blog/category.htmi'
    context_object_name = 'page_obj'
    paginate_by = PAGINATOR_CATEGORY

    def get_context_data(self, **kwargs):
        return dict(
            super().get_context_data(**kwargs),
            category=self.category
        )

    def get_queryset(self):
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True,
            pub_date__lte=datetime.now()
        )
        return self.category.posts.all()

