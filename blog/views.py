from django.shortcuts import render, redirect
from .models import Post, Contact, Comment, Category, Tag
from django.core.paginator import Paginator
import requests

BOT_TOKEN = '6380957235:AAHOgqvvnffZL4deU_pY79mieYdBJYr0J-w'
CHAT_ID = '1624671606'


def home_view(request):
    data = request.GET
    page = data.get('page', 1)
    more_posts = Post.objects.all()
    tags = Tag.objects.all()
    categories_name = Category.objects.all()
    posts = Post.objects.filter(is_published=True).order_by('created_at')[:3]
    page_obj = Paginator(more_posts, 4)
    d = {
        'posts': posts,
        'more_posts': page_obj.get_page(page),
        'home': 'active',
        'categories_name': categories_name,
        'tags': tags

    }
    return render(request, 'index.html', context=d)


def about_view(request):
    posts = Post.objects.filter(is_published=True).order_by('created_at')[:3]
    tags = Tag.objects.all()
    categories_name = Category.objects.all()
    d = {
        'posts': posts,
        'about': 'active',
        'categories_name': categories_name,
        'tags': tags
    }
    return render(request, 'about.html', context=d)


def detail_view(request, pk):
    post = Post.objects.filter(id=pk).first()
    posts = Post.objects.filter(is_published=True).order_by('created_at')[:3]
    tags = Tag.objects.all()
    comments = Comment.objects.filter(post_id=pk, is_published=True)
    d = {
        'post': post,
        'posts': posts,
        'comments': comments,
        'comments_num': len(comments),
        'blog': 'active',
        'tags': tags
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
    posts = Post.objects.filter(is_published=True, category_id=cat)
    categories_name = Category.objects.all()
    tags = Tag.objects.all()

    d = {
        'category': 'active',
        'categ': categ,
        'posts': posts,
        'categories_name': categories_name,
        'tags': tags

    }

    return render(request, 'category.html', context=d)


def contact_view(request):
    posts = Post.objects.filter(is_published=True).order_by('created_at')[:3]
    categories_name = Category.objects.all()
    tags = Tag.objects.all()
    d = {
        'posts': posts,
        'contact': 'active',
        'categories_name': categories_name,
        'tags': tags
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
    posts = Post.objects.filter(is_published=True, title__icontains=query)
    tags = Tag.objects.all()
    d = {
        'posts': posts,
        'tags': tags
    }
    return render(request, 'category.html', context=d)


def tag_view(request):
    data = request.GET
    tag_id = data.get('tag', None)
    categories = Category.objects.all()
    tags = Tag.objects.all()

    if tag_id:
        posts = Post.objects.filter(is_published=True, tag=tag_id)
    else:
        posts = Post.objects.filter(is_published=True)

    d = {
        'posts': posts,
        'categories': categories,
        'tags': tags
    }
    return render(request, 'index.html', context=d)
