from django.urls import path
from .views import home_view, about_view, category_view, contact_view, detail_view, search_view, tag_view

urlpatterns = [
    path('', home_view),
    path('about/', about_view),
    path('blog/<int:pk>', detail_view),
    path('category/', category_view),
    path('contact/', contact_view),
    path('search/', search_view),
    path('tag/', tag_view)
]