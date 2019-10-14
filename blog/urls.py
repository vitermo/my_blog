from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('<int:blog_id>/', views.detail, name='blog_detail'),
    path('category/<int:category_id>', views.catagory, name='blog_category'),
    path('tag/<int:tag_id>', views.tag, name='blog_tag'),
    path('search/', views.search, name='blog_search'),
    path('archives/<int:year>/<int:month>', views.archives, name='blog_archives')
]
