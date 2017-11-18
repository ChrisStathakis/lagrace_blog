"""lagrace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from homepage.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap

from products.views import *

sitemaps = {
    'category':CategorySitemap,
    'store':StoreSitemap,
}

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', view=homepage, name='homepage'),
    url(r'^blog/$', PostPage.as_view(), name='blog'),
    url(r'^blog-detail/(?P<slug>[-\w]+)/$', PostDetail.as_view(), name='blog_detail'),
    url(r'^stores/$', StoresPage.as_view(), name='stores'),
    url(r'^store-detail/(?P<slug>[-\w]+)/$', StorePage.as_view(), name='store_detail'),
    url(r'^about/$', PostPage.as_view(), name='about'),


    url(r'^admin-control/$', view=admin_control, name='admin_control'),
    url(r'^robots\.txt$', include('robots.urls')),
    url(r'^sitemap\.xml',sitemap, {'sitemaps': sitemaps}),
    


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#handler404 = 'homepage.views.custom_404'