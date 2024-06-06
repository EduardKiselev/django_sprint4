from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category, Profile
from datetime import datetime
from django.views.generic import DetailView, ListView


class PostListView(ListView):
    model = Post


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
            '-pub_date',)[:5]
    context = {
        'post_list': post_list
    }
    return render(request, template, context)


def post_detail(request, id):
    post_list =\
        Post.objects.select_related(
            'category',
            'author',
            'location').\
        filter(
            pub_date__lt=datetime.now(),
            is_published=True,
            category__is_published=True)
    post = get_object_or_404(post_list, id=id)
    template = 'blog/detail.html'
    context = {'post': post}
    return render(request, template, context)


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
            category__is_published=True)
    context = {'category': category, 'post_list': post_list}
    return render(request, template, context)


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'blog/profile.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
        
    #     context['get_full_name'] = context['first_name'] + ' ' + context['second_name']
        