from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import CommentForm, PostForm, UserForm, PasswordChangeForm
from .models import Category, Post, Comment

User = get_user_model()


POSTS_AMOUNT = 10
CATEGORIES_AMOUNT = 10


class PostsDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['commentaries'] = (
            self.object.comments.prefetch_related('post')
        )
        return context


class PostsCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={
                           'username': self.request.user.get_username()
                       }
                       )


class PostsUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def get_object(self, **kwargs):
        post = get_object_or_404(
            Post,
            pk=self.kwargs.get('post_id'),
            author=self.request.user)
        return post

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Post, pk=kwargs['post_id'], author=request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', self.kwargs['post_id'])


class PostsDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')

    def get_object(self, **kwargs):
        return get_object_or_404(
            Post,
            pk=self.kwargs.get('post_id'),
            author=self.request.user)


class PostsListView(ListView):
    model = Post
    template_name = 'blog/index.html'

    queryset = Post.objects.select_related(
        'location',
        'category').filter(is_published=True,
                           category__is_published=True,
                           pub_date__lte=datetime.now())
    paginate_by = POSTS_AMOUNT


class CategoryListView(ListView):
    model = Category
    paginate_by = CATEGORIES_AMOUNT
    category = None

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category, category_slug=kwargs['slug'])
        if not self.category.is_published:
            raise Http404('Страница не найдена')
        return super().dispatch(request, *args, **kwargs)


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    comment = None

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.comment = self.comment
        return super().form_valid(form)


class CommentUpdateView(CreateView):
    model = Comment
    form_class = CommentForm


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    success_url = reverse_lazy('blog:list')


class ProfileDetailView(DetailView):
    model = User
    template_name = 'blog/profile.html'
    profile = None

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
                'location').filter(author=self.request.user)
        )
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm

    def get_object(self, **kwargs):
        return get_object_or_404(User, username=self.kwargs.get('username'))


class UserUpdateView(UpdateView):
    form_class = UserForm
    model = User
    template_name = 'blog/user.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class UserPasswordUpdateView(UserUpdateView):
    form_class = PasswordChangeForm
    model = User
