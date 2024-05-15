from django.db.models import Count
from django.shortcuts import render, redirect
from .models import Post, Contact, Comment, Category, Tag
from django.core.paginator import Paginator
import requests

BOT_TOKEN = '6380957235:AAHOgqvvnffZL4deU_pY79mieYdBJYr0J-w'
CHAT_ID = '1624671606'


def home_view(request):
    data = request.GET
    page = data.get('page', 1)
    more_posts = Post.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')[:3]
    tags = Tag.objects.all()
    all_posts = Post.objects.annotate(num_comments=Count('comments'))
    categories_name = Category.objects.annotate(num_posts=Count('posts'))
    posts = Post.objects.annotate(num_comments=Count('comments')).order_by('-created_at')[:3]
    latest_posts = Post.objects.annotate(num_comments=Count('comments')).order_by('-created_at')[:3]
    page_obj = Paginator(all_posts, 4)
    d = {
        'posts': posts,
        'more_posts': more_posts,
        'home': 'active',
        'categories_name': categories_name,
        'tags': tags,
        'all_posts': page_obj.get_page(page),
        'latest_posts': latest_posts

    }
    return render(request, 'index.html', context=d)


def about_view(request):
    data = request.GET
    page = data.get('page', 1)
    posts = Post.objects.annotate(num_comments=Count('comments')).order_by('-created_at')[:3]
    tags = Tag.objects.all()
    latest_posts = Post.objects.annotate(num_comments=Count('comments')).order_by('-created_at')[:3]
    categories_name = Category.objects.annotate(num_posts=Count('posts'))
    more_posts = Post.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')[:3]
    page_obj = Paginator(latest_posts, 4)
    d = {
        'posts': posts,
        'latest_posts': page_obj.get_page(page),
        'about': 'active',
        'categories_name': categories_name,
        'tags': tags,
        'more_posts': more_posts

    }
    return render(request, 'about.html', context=d)


def detail_view(request, pk):
    post = Post.objects.filter(id=pk).first()
    latest_posts = Post.objects.annotate(num_comments=Count('comments')).order_by('-created_at')[:3]
    tags = Tag.objects.all()
    categories_name = Category.objects.annotate(num_posts=Count('posts'))
    more_posts = Post.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')[:3]
    comments = Comment.objects.filter(post_id=pk, is_published=True)
    d = {
        'post': post,
        'latest_posts': latest_posts,
        'comments': comments,
        'comments_num': len(comments),
        'blog': 'active',
        'tags': tags,
        'categories_name': categories_name,
        'more_posts': more_posts
    }
    if request.method == 'POST':
        data = request.POST
        obj = Comment.objects.create(name=data['name'], email=data['email'], message=data['message'],
                                     post_id=pk)
        obj.save()
        return redirect(f'/blog/{pk}')
    return render(request, 'blog-single.html', context=d)


def category_view(request):
    data = request.GET
    cat = data.get('cat', None)
    categ = Category.objects.filter(id=cat).first()
    posts = Post.objects.annotate(num_comments=Count('comments')).filter(category_id=cat)
    latest_posts = Post.objects.annotate(num_comments=Count('comments')).order_by('-created_at')[:3]
    more_posts = Post.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')[:3]
    categories_name = Category.objects.annotate(num_posts=Count('posts'))
    tags = Tag.objects.all()

    d = {
        'category': 'active',
        'categ': categ,
        'posts': posts,
        'categories_name': categories_name,
        'tags': tags,
        'more_posts': more_posts,
        'latest_posts': latest_posts

    }

    return render(request, 'category.html', context=d)


def contact_view(request):
    latest_posts = Post.objects.annotate(num_comments=Count('comments')).order_by('-created_at')[:3]
    categories_name = Category.objects.annotate(num_posts=Count('posts'))
    more_posts = Post.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')[:3]
    tags = Tag.objects.all()
    d = {
        'latest_posts': latest_posts,
        'contact': 'active',
        'categories_name': categories_name,
        'tags': tags,
        'more_posts': more_posts
    }
    if request.method == 'POST':
        data = request.POST
        obj = Contact.objects.create(name=data['name'], email=data['email'],
                                     phone=data['phone'], message=data['message'])
        obj.save()
        text = f'''
        project: BALITA
        id: {obj.id}
        name: {obj.name}
        email: {obj.email}
        phone: {obj.phone}
        message: {obj.message}
        timestamp: {obj.created_at}
        '''
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}'
        requests.get(url)
        return redirect('/contact')
    return render(request, 'contact.html', context=d)


def search_view(request):
    if request.method == "POST":
        date = request.POST
        query = date['query']
        return redirect(f'/search?q={query}')

    query = request.GET.get('q')
    categories_name = Category.objects.annotate(num_posts=Count('posts'))
    posts = Post.objects.annotate(num_comments=Count('comments')).filter(is_published=True, title__icontains=query)
    latest_posts = Post.objects.annotate(num_comments=Count('comments')).order_by('-created_at')[:3]
    more_posts = Post.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')[:3]
    tags = Tag.objects.all()
    d = {
        'posts': posts,
        'tags': tags,
        'categories_name': categories_name,
        'latest_posts': latest_posts,
        'more_posts': more_posts
    }
    return render(request, 'search.html', context=d)


def tag_view(request):
    data = request.GET
    tag_id = data.get('tag', None)
    categories_name = Category.objects.annotate(num_posts=Count('posts'))
    more_posts = Post.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')[:3]
    latest_posts = Post.objects.annotate(num_comments=Count('comments')).order_by('-created_at')[:3]
    tags = Tag.objects.all()
    tag = Tag.objects.filter(id=tag_id).first()

    if tag_id:
        posts = Post.objects.annotate(num_comments=Count('comments')).filter(is_published=True, tag=tag_id)
    else:
        posts = Post.objects.annotate(num_comments=Count('comments')).filter(is_published=True)

    d = {
        'posts': posts,
        'categories_name': categories_name,
        'tags': tags,
        'tag': tag,
        'more_posts': more_posts,
        'latest_posts': latest_posts
    }
    return render(request, 'tag.html', context=d)
