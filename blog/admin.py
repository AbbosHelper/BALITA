from django.contrib import admin
from .models import Post, Category, Contact, Comment, Tag


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    fields = ('name', 'email', 'message')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    list_display_links = ('id', 'name')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'is_published', 'created_at')
    list_display_links = ('id', 'title')
    inlines = (CommentInline, )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    list_display_links = ('id', 'name')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email')
    list_display_links = ('id', 'name')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'is_published')
    list_display_links = ('id', 'name')
