from django.contrib.sitemaps import Sitemap
from .models import *
from my_stores.models import *
class CategorySitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Category.objects.all()

class StoreSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Store.objects.all()
