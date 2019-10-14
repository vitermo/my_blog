"""woniu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from blog.feed import LatestEntriesFeed
from blog import views
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from blog.models import Entry

info_dict = {
    'queryset': Entry.objects.all(),
    'date_field': 'modifyed_time'
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index,name='blog_index'),
    path('blog/', include('blog.urls')),
    path('latest/feed/', LatestEntriesFeed()),
    path('comment/',include('comment.urls')),
    re_path(r'^sitemap\.xml$', sitemap, {'sitemaps': {'blog': GenericSitemap(info_dict, priority=0.6)}},
      name='django.contrib.sitemaps.views.sitemap'),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  #添加图片的url

handler403 = views.permission_denied
handler404 = views.page_not_found
handler500 = views.page_error
