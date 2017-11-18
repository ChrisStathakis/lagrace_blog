from django.contrib import admin
from .models import *
# Register your models here.


class PhonesInline(admin.TabularInline):
    model = StorePhone
    extra = 2

class GalleryPhotoInline(admin.TabularInline):
    model = StoreGallery
    extra = 5
        

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['title', 'latitude', 'longitude']
    inlines = [PhonesInline, GalleryPhotoInline]
    fieldsets = (
        ('Βασικά Χαρακτηριστικά', {
            'fields': ('active', 'title',)
        }),
        ('Στοιχεία Σελίδας', {
            'classes': ('collapse',),
            'fields': (
                       ('text',),
                       ('address', 'latitude', 'longitude'),
                       )
        }),
    )


@admin.register(StoreGallery)
class StoreGalleryAdmin(admin.ModelAdmin):
    list_display = ['tiny_image_tag', 'store_related', 'active', 'main_image']
    list_filter = ['store_related__title', 'title' ]
    fields = ('active', 'title', 'image', 'main_image', 'store_related', 'alt')
    readonly_fields = ['tiny_image_tag']
    list_per_page = 10


@admin.register(StoreServices)
class StoreServicesAdmin(admin.ModelAdmin):
    list_display = ['title', 'page_related']
    list_filter = ['page_related']

admin.site.register(StorePhone)
admin.site.register(StoreWork)
