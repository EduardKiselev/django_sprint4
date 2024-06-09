from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Category, Comment, User
from blog.forms import CommentForm, ProfileForm
from datetime import datetime
from django.views.generic import DetailView, DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required


class OnlyAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


def profile(request, username):
    template = 'blog/profile.html'
    profile = get_object_or_404(User, username=username)
    print('req:', request.user, 'username:', username)
    if request.user.username == username:
        all_posts = Post.objects.select_related(
            'category',
            'author',
            'location').\
            filter(
                author__username=username).\
            order_by(
                '-pub_date',)
    else:
        all_posts = Post.objects.select_related(
            'category',
            'author',
            'location').\
            filter(
                pub_date__lt=datetime.now(),
                is_published=True,
                category__is_published=True,
                author__username=username).\
            order_by(
                '-pub_date',)
    all_posts = all_posts.annotate(comment_count=Count('comment'))
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'profile': profile, 'page_obj': page_obj}
    return render(request, template, context)


@login_required
def profile_update(request):
    template = 'blog/user.html'
    instance = get_object_or_404(User, username=request.user)
    form = ProfileForm(request.POST or None, instance=instance)
    context = {'form': form}
    if form.is_valid():
        form.save()
        return redirect('blog:index')
    return render(request, template, context)


def index(request):
    template = 'blog/index.html'
    post_list =\
        Post.objects.select_related(
            'category',
            'author',
            'location').\
        filter(
            pub_date__lt=datetime.now(),
            is_published=True,
            category__is_published=True).\
        order_by(
            '-pub_date',)
    post_list = post_list.annotate(comment_count=Count('comment'))
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, template, context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        comments = Comment.objects.filter(
            post=self.kwargs.get(self.pk_url_kwarg)).order_by(
                'created_at')
        context['comments'] = comments
        return context

    def form_valid(self, form):
        form.instance.post = get_object_or_404(
            Post, id=self.kwargs.get(self.pk_url_kwarg))
        form.instance.author = get_object_or_404(
            User, username=self.request.user)
        return super().form_valid(form)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(Category, slug=category_slug,
                                 is_published=True)
    post_list =\
        Post.objects.select_related(
            'category',
            'author',
            'location').\
        filter(
            category=category,
            pub_date__lt=datetime.now(),
            is_published=True,
            category__is_published=True).order_by(
            '-pub_date',)
    post_list = post_list.annotate(comment_count=Count('comment'))
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'category': category, 'page_obj': page_obj
    }
    return render(request, template, context)


class PostDeleteView(OnlyAuthorMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')


class PostUpdateView(OnlyAuthorMixin, UpdateView):
    model = Post
    template_name = 'blog/create.html'
    fields = ['title', 'text', 'pub_date', 'location', 'category', 'image']

    def get_success_url(self):
        print(self.kwargs.get(self.pk_url_kwarg))
        return reverse_lazy('blog:post_detail',
                            args=(self.kwargs.get(self.pk_url_kwarg),))


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'text', 'pub_date', 'location', 'category', 'image']
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:profile',
                            args=(self.request.user.username,))


class CommentDeleteView(OnlyAuthorMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            args=(self.kwargs.get('id'),))


class CommentUpdateView(OnlyAuthorMixin, UpdateView):
    model = Comment
    fields = ['text', ]
    template_name = 'blog/comment.html'

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            args=(self.kwargs.get('id'),))


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            args=(self.kwargs.get(self.pk_url_kwarg),))

    def form_valid(self, form):
        form.instance.post = get_object_or_404(
            Post, id=self.kwargs.get(self.pk_url_kwarg))
        form.instance.author = self.request.user

        return super().form_valid(form)
