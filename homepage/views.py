from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, render_to_response, redirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib import messages
from django.views.generic import ListView, DetailView, FormView
from django.template import RequestContext
from .models import *
from my_stores.models import *
from blog.models import *
from products.models import *
from contact.forms import ContactForm
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.

def initial_data(page_request=None):
    index_page = Homepage.objects.filter(active=True).last()
    stores = Store.objects.all()
    brands = Brands.objects.all()[:10]
    store_gallery = []
    return index_page, stores, brands, store_gallery




#  Views Start here!!

def custom_404(request):
    return render(request, 'solec/page404.html', {}, status=404)

def homepage(request):
    index_page, stores, brands, store_gallery = initial_data()
    page_title, page_keywords, page_description = index_page.title, index_page.keywords, index_page.description
    banners = MainBanner.my_query.active_and_related(related_page=index_page)
    posts = Post.my_query.active_posts()
    blog_category = BlogCategory.objects.filter(active=True)
    circe_images = CircleImages.objects.filter(active=True)[:3]
    instagram_feed = InstagramFeed.objects.all()
    context = locals()
    return render(request, 'solec/index.html', context)


class PostPage(ListView):
    model = Post
    template_name = 'solec/blog-grid.html'
    paginate_by = 4

    def get_queryset(self):
        queryset = Post.my_query.active_posts()
       
        if self.request.GET:        
            search_pro = self.request.GET.get('search_pro')
            cate_name = self.request.GET.getlist('cate_name')
            queryset = queryset.filter(category__id__in=cate_name) if cate_name else queryset
            if search_pro:
                queryset = queryset.filter(Q(title__icontains=search_pro) |
                                        Q(category__title__icontains=search_pro)
                                        ).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        blog_page= True
        context = super(PostPage, self).get_context_data(**kwargs)
        index_page, stores, brands, store_gallery = initial_data()
        page_title, page_keywords, page_description = '%s | %s' % (index_page.title, index_page.blog_title), index_page.blog_keywords, index_page.blog_description
        page_bread = 'Blog'
        blog_categories = BlogCategory.objects.all()
        cate_name = self.request.GET.getlist('cate_name', None)
        search_pro = self.request.GET.get('search_pro')
        context.update(locals())
        print(cate_name)
        return context
    


class PostDetail(DetailView):
    model = Post
    slug_field = 'slug'
    template_name = 'solec/blog-detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        index_page, stores, brands, store_gallery = initial_data()
        page_title, page_keywords, page_description = ['%s | %s' %(index_page.title, self.object),
                                                    index_page.keywords,
                                                    index_page.description
                                                    ]
        post_brands = Brands.objects.filter(active=True, post_related=self.object)
        gallery = Gallery.objects.filter(active=True,
                                        brand_related__in=post_brands,
                                        post_related = self.object)
        context.update(locals())
        return context
        

class StoresPage(ListView):
    model = Store
    template_name = 'solec/blog-grid.html'

    def get_context_data(self, **kwargs):
        store_page = True
        context = super(StoresPage, self).get_context_data(**kwargs)
        index_page, stores, brands, store_gallery = initial_data()
        page_title, page_keywords, page_description = '%s | %s' %(index_page.title, index_page.store_title), index_page.store_keywords, index_page.store_description
        page_bread = 'Καταστήματα'
        context.update(locals())
        return context


class StorePage(DetailView):
    model = Store
    slug_field = 'slug'
    template_name = 'solec/aboutus.html'

    def get_context_data(self, **kwargs):
        context = super(StorePage, self).get_context_data(**kwargs)
        index_page, stores, brands, store_gallery = initial_data()
        page_title, page_keywords, page_description = ['%s | %s' %(index_page.title, self.object.title),
                                                    index_page.keywords,
                                                    index_page.description
                                                    ]
        print(page_title)
        phones = StorePhone.objects.filter(store_related=self.object)
        image_photos = self.object.all_images()
        form = ContactForm()
        context.update(locals())
        return context
    
    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ευχαριστούμε για την ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        context.update(locals())
        return context

   
class NewProducts(ListView):
    model = Product
    template_name = 'solec/shop-grid.html'
    paginate_by = 15
    initial_products = ''

    def get_queryset(self):
        queryset = Product.my_query.active_products()
        self.initial_products = queryset[:120]
        if self.request.GET:
            search_pro, brand_name, category_name = get_filters_values(self.request)
            queryset = filters_query(queryset, search_pro, brand_name, category_name)
        return queryset

    def get_context_data(self, **kwargs):
        new_products_page = True
        context = super(NewProducts, self).get_context_data(**kwargs)
        index_page, stores, brands, store_gallery = initial_data()
        brands, site_cate = extract_filters(self.initial_products)
        #page_title, keywords, description = index_page.new_products_title, index_page.new_products_keywords, index_page.new_products_description
        popular_products, featured_products = Product.my_query.popular(), Product.my_query.featured()
        if self.request.GET:
            search_pro, brand_name, category_name, color_name = get_filters_values(self.request)
        context.update(locals())
        return context



class ContestPage(FormView):
    pass



class CategoryPage(ListView):
    model = Product
    slug_field = 'slug'
    paginate_by = 15
    context_object_name = 'articles'
    template_name = 'solec/shop-grid.html'
    initial_products = ''
    childs, get_category = [], ''

    def get_queryset(self):
        self.get_category = Category.objects.get(slug=self.kwargs['slug'])
        queryset = Product.my_query.active_products_category(self.get_category)
        self.initial_products = queryset
        if self.request.GET:
            search_pro, brand_name, category_name = get_filters_values(self.request)
            queryset = filters_query(queryset, search_pro, brand_name, category_name)
        return queryset

    def get_context_data(self, **kwargs):
        category_page = True
        context = super(CategoryPage, self).get_context_data(**kwargs)
        index_page, stores, brands, store_gallery = initial_data()
        brands, site_cate = extract_filters(self.initial_products)
        # page_title, keywords, description = self.get_category.title, self.get_category.meta_keywords, self.get_category.meta_description
        popular_products, featured_products = Product.my_query.popular(), Product.my_query.featured_products_by_category(self.get_category)
        if self.request.GET:
            search_pro, brand_name, category_name, color_name = get_filters_values(self.request)
        context.update(locals())
        return context


@staff_member_required
def admin_control(request):
    products = Product.objects.all()[:20]
    brands = Brand.objects.all()
    categories = Category.objects.all()
    stores = Store.objects.all()
    store_name = None
    category_name = None
    brands_name = None
    if request.GET:
        products = Product.objects.all()
        brands_name = request.GET.getlist('brand_name')
        category_name = request.GET.getlist('category_name')
        store_name = request.GET.getlist('store_name')
        search_pro = request.GET.get('search_pro')
        products = products.filter(title__icontains=search_pro) if search_pro else products
        products = products.filter(brand__id__in = brands_name) if brands_name else products
        products = products.filter(category__id__in = category_name) if category_name else products
        products = products.filter(store_related__id__in = store_name) if store_name else products
    if 'active_product' in request.POST:
        query_set = request.POST.getlist('query_set')
        if query_set:
            for ele in query_set:
                product = Product.objects.get(id=ele)
                product.active = True
                product.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if 'de_active_product' in request.POST:
        query_set = request.POST.getlist('query_set')
        if query_set:
            for ele in query_set:
                product = Product.objects.get(id=ele)
                product.active = False
                product.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if 'active_first_page' in request.POST:
       query_set = request.POST.getlist('query_set')
       if query_set:
           for ele in query_set:
               product = Product.objects.get(id=ele)
               product.first_page = True
               product.save()
           return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if 'de_active_first_page' in request.POST:
       query_set = request.POST.getlist('query_set')
       if query_set:
           for ele in query_set:
               product = Product.objects.get(id=ele)
               product.first_page = False
               product.save()
           return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if 'choose_brand' in request.POST:
        query_set = request.POST.getlist('query_set')
        brand_id = request.POST.get('brand_id')
        if query_set and brand_id:
            new_brand = Brand.objects.get(id=brand_id)
            for ele in query_set:
                product = Product.objects.get(id=ele)
                product.brand = new_brand
                product.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if 'choose_cate' in request.POST:
        query_set = request.POST.getlist('query_set')
        cate_id = request.POST.get('cate_id')
        if query_set and cate_id:
            new_cat = Category.objects.get(id=cate_id)
            for ele in query_set:
                product = Product.objects.get(id=ele)
                product.category = new_cat
                product.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if 'choose_store' in request.POST:
        query_set = request.POST.getlist('query_set')
        store_id = request.POST.getlist('store_id')
        if query_set and store_id:
            for store in store_id:
                new_store = Store.objects.get(id=store)
                for ele in query_set:
                    product = Product.objects.get(id=ele)
                    product.store_related.add(new_store)
                    product.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if 'remove_store' in request.POST:
        query_set = request.POST.getlist('query_set')
        store_id = request.POST.getlist('store_id')
        if query_set and store_id:
            for store in store_id:
                new_store = Store.objects.get(id=store)
                for ele in query_set:
                    product = Product.objects.get(id=ele)
                    product.store_related.remove(new_store)
                    product.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    paginator = Paginator(products, 250) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    context = locals()
    return render(request, 'admin_section.html', context)

