from datetime import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from .froms import PostForm, CommentForm
from .models import Category, Post, Comment
from django.views.generic import CreateView, ListView, DetailView, UpdateView

# main page view settings
POSTS_PAGINATION = 10
POSTS_ORDERING = 'pub_date'
PAGINATOR_CATEGORY = 10

User = get_user_model()


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, id=self.kwargs['pk'])
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = [
        'title',
        'text',
        'location',
        'category',
    ]
    success_url = reverse_lazy('blog:index')


class PostCategoryView(ListView):
    model = Post
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


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Post, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


class CommentCreateView(LoginRequiredMixin, CreateView):
    post = None
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.post = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post:post_detail', kwargs={'pk': self.post.pk})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Comment, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(User, id=kwargs['user_id'], author=request.user)
        return super().dispatch(request, *args, **kwargs)
