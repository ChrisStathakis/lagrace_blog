from django.contrib import admin
from .models import Contact
# Register your models here.


def read_or_not(modeladmin, request, queryset):
    for ele in queryset:
        if ele.is_readed:
            ele.is_readed = False
        else:
            ele.is_readed = True
        ele.save()
read_or_not.short_description = 'Διαβασμένο ή Όχι'

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    actions = [read_or_not, ]
    readonly_fields =['day_added']
    list_display = ['subject', 'email', 'day_added', 'is_readed']
    list_filter =['is_readed']
