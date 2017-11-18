from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
# Register your models here.


def show_first_page(modeladmin, request, queryset):
    for product in queryset:
        if product.first_page:
            product.first_page = False
        else:
            product.first_page = True
        product.save()
show_first_page.short_description = 'Ενεργοποίηση/Απενεργοποίηση Εμφάνιση στην Αρχική Σελίδα'

def active_deactive_products(modeladmin, request, queryset):
    for product in queryset:
        if product.active:
            product.active = False
        else:
            product.active = True
        product.save()
active_deactive_products.short_description = 'Ενεργοποίηση/Απενεργοποίηση Προϊόντος'


class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 2

class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ['product_related', 'active', 'main_photo']
    list_filter = ['active']
    search_fields =['product_related__title', 'product_related__category__title', 'product_related__store__title']
    fields = ('active', 'title', 'image', 'product_related', 'main_photo')

class ProductAdmin(ImportExportModelAdmin):
    list_display = ['tiny_image_tag', 'title', 'active', 'first_page', 'category', 'brand']
    list_filter = ['active', 'first_page', 'category', 'brand', 'store_related']
    search_fields = ('title', 'brand__title', 'category__title', 'store_related__title')
    readonly_fields = ['tiny_image_tag']
    list_per_page = 15
    inlines = [ProductGalleryInline,]
    actions = [active_deactive_products, show_first_page]
    fieldsets = (
        ('Βασικά Χαρακτηριστικά', {
            'fields': (('active', 'first_page', 'popular', 'featured'),'title',
             ('tiny_image_tag', 'image_href'),
             'text',
             ('store_related', 'category', 'brand'),
             ('price', 'price_discount'),
             'my_moda',)
        }),
        ('SEO', {
            'classes': ('collapse',),
            'fields': ('slug',),
        }),
    )

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ['title', 'active', 'first_page', 'href']
    list_filter = ['active', ]
    search_fields = ('title', )

@admin.register(Brand)
class BrandAdmin(ImportExportModelAdmin):
    list_display = ['title', 'active',]
    list_filter = ['active',]
    search_fields = ('title',)

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductGallery, ProductGalleryAdmin)
admin.site.register(CategoryServices)
