from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .forms import CommentForm, PostForm, UserForm, PasswordChangeForm
from .models import Category, Post, Comment

User = get_user_model()


POSTS_AMOUNT: int = 10
CATEGORIES_AMOUNT: int = 10


class PostsDetailView(DetailView):
    model = Post
    form_class = CommentForm
    blog_post = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.prefetch_related(
            'blog_post'
        ).filter(
            blog_post=blog_post
        )
        context['comment_count'] = len(context['comments'])
        return context


class PostsCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={
                'username': self.request.user.get_username()
            }
        )


class PostsUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def get_object(self, **kwargs):
        return get_object_or_404(
            Post,
            pk=self.kwargs.get('post_id'),
            author=self.request.user)

    def form_valid(self, form):
        if form.is_valid():
            form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            self.kwargs['post_id']
        )


class PostsDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')
    template_name = 'blog/post_form.html'

    def get_object(self, **kwargs):
        return get_object_or_404(
            Post,
            pk=self.kwargs.get('post_id'),
            author=self.request.user)


class PostsListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by: int = POSTS_AMOUNT

    queryset = Post.objects.select_related(
        'location',
        'category',
    ).filter(is_published=True,
             category__is_published=True,
             pub_date__lte=datetime.now())


class CategoryListView(ListView):
    model = Category
    paginate_by = CATEGORIES_AMOUNT
    category = None

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(
            Category,
            slug=kwargs['category_slug'],
            is_published=True,
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_obj'] = (
            Post.objects.prefetch_related(
                'category',).filter(
                category=self.category.id,
                is_published=True,
            )
        )
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    blog_post = None
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.blog_post = get_object_or_404(
            Post,
            pk=kwargs['post_id']
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.blog_post = self.blog_post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'pk': self.kwargs['post_id']}
        )


class CommentUpdateView(LoginRequiredMixin, CreateView):
    blog_post = None
    comment = None
    model = Comment
    form_class = CommentForm

    def get_object(self, **kwargs):
        return get_object_or_404(
            Comment,
            pk=self.kwargs.get('comment_id'),
            author=self.request.user)

    '''def dispatch(self, request, *args, **kwargs):
        self.blog_post = Post.objects.get(pk=self.kwargs['post_id'])
        self.comment = Comment.objects.get(pk=self.kwargs['comment_id'])
        return super().dispatch(request, *args, **kwargs)'''

    def form_valid(self, form):
        if form.is_valid():
            form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            self.kwargs['post_id']
        )


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    success_url = reverse_lazy('blog:list')


class UserDetailView(DetailView):
    model = User
    template_name = 'blog/profile.html'
    user = None

    def dispatch(self, request, *args, **kwargs):
        self.user = get_object_or_404(
            User,
            username=kwargs['username']
        )
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, **kwargs):
        return get_object_or_404(User,
                                 username=self.kwargs.get(
                                     'username')
                                 )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_obj'] = (
            Post.objects.prefetch_related(
                'author',
                'category',
                'location').filter(
                author=self.request.user
            ).order_by('-pub_date')
        )
        context['profile'] = User.objects.get(username=self.user.get_username())
        return context

    paginate_by: int = POSTS_AMOUNT


class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserForm
    model = User
    template_name = 'blog/user.html'
    user = None

    def dispatch(self, request, *args, **kwargs):
        self.user = get_object_or_404(
            User,
            username=kwargs['username']
        )
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(
            User,
            username=self.kwargs.get(
                'username')
        )

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.user.get_username()}
        )


class UserPasswordUpdateView(UserUpdateView):
    form_class = PasswordChangeForm
    model = User
    template_name = 'registration/password_reset_form.html'
