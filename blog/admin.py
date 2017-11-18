from django.contrib import admin
from .models import *
# Register your models here.





@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
	search_fields = ['title',]
	readonly_fields = ['tiny_tag_image', 'tiny_tag_carousel_image']
	list_display = ['tiny_tag_image', 'title', 'active']
	list_filter = ['active']
	fieldsets = (
        ('Βασικά Χαρακτηριστικά', {
            'fields': (('active', 'title'), ('css_class', 'slug'))
        }),
        ('Στοιχεία Σελίδας', {
            'fields': (
                       ('tiny_tag_image', 'image'),
                       ('tiny_tag_carousel_image', 'carousel_image'),
                       )
        }),
    )


@admin.register(Brands)
class BrandsAdmin(admin.ModelAdmin):
	search_fields = ['title', ]
	list_per_page = 10
	readonly_fields = ['tiny_tag_image',]
	list_display = ['tiny_tag_image', 'title', 'active']
	list_filter = ['active', 'post_related',]

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
	search_fields = ['title', 'post_related__title', 'brand_related__title']
	list_per_page = 10
	readonly_fields = ['tiny_tag_image',]
	list_display = ['tiny_tag_image', 'title', 'post_related', 'active']
	list_filter = ['active', 'post_related', 'brand_related']



class GalleryInline(admin.TabularInline):
	model = Gallery
	readonly_fields = ['tiny_tag_image',]
	list_display = ['tiny_tag_image', 'image', 'title', 'active']
	extra = 5
	
class BrandsInline(admin.TabularInline):
	model = Brands.post_related.through
	exclude = ['alt']
	extra = 5

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	inlines = [BrandsInline, GalleryInline, ]
	readonly_fields = ['date_added', 'tiny_image', 'date_edited']
	list_display = ['title', 'active','featured', 'category', 'date_added']
	list_filter = ['active', 'category', 'date_added', 'featured']
	fieldsets = (
        ('Βασικά Χαρακτηριστικά', {
            'fields': (('active', 'featured'),
             ('title', 'category'),
             ('tiny_image', 'image'),
             ('context'),
             ('date_added', 'date_edited'),
             )
        }),
        ('SEO', {
            'classes': ('collapse',),
            'fields': ('slug', 'keywords', 'meta_description'),
        }),
    )