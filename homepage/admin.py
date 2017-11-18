from django.contrib import admin
from .models import *

# Register your models here.

class BannerMessagesInline(admin.TabularInline):
    model = BannerMessages
    extra = 3

class MainBannerInline(admin.TabularInline):
    model = MainBanner
    extra = 1

class MainBannerAdmin(admin.ModelAdmin):
    display_list = ['title', 'active', 'page_related']
    filter_list = ['active', 'page_related']


class HomepageAdmin(admin.ModelAdmin):
    readonly_fields = ['tiny_background_image', 'tiny_circle_image']
    display_list = ['title', 'active',]
    filter_list = ['active']
    inlines = [MainBannerInline, BannerMessagesInline]
    fieldsets = (
        ('Βασικά Χαρακτηριστικά', {
            'fields': (
                ('title', 'keywords', 'description'),
                ('tiny_background_image','background_image'),
                ('tiny_circle_image', 'circle_image')
                )
        }),
        ('Διαχείρηση υπόλοιπων Σελίδων', {
            'classes': ('collapse',),
            'fields': (
                ('blog_title', 'blog_keywords', 'blog_description'),
                ('store_title', 'store_keywords', 'store_description'),
                ('about_title', 'about_keywords', 'about_description'),
                ),
        }),
    )
    

@admin.register(CircleImages)
class CircleImagesAdmin(admin.ModelAdmin):
    pass

@admin.register(InstagramFeed)
class InstagramFeedAdmin(admin.ModelAdmin):
    pass


admin.site.register(Homepage, HomepageAdmin)
admin.site.register(MainBanner, MainBannerAdmin)
admin.site.register(BannerMessages)
admin.site.register(IconMessages)
admin.site.register(ContactInfo)
admin.site.register(Phones)
