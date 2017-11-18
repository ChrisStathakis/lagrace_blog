from django.db import models
from my_stores.models import Store
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
# Create your models here.

class BannerManager(models.Manager):
    def active_and_related(self, related_page):
        return super(BannerManager, self).filter(active=True, related_page=related_page)


def upload_location(instance, filename):
    return 'main_banners/%s/%s' % (instance.title, filename)

def upload_background_banner(instance, filename):
    return 'background_banners/%s/%s' % (instance.title, filename)

def validate_size(value):
    if value.file.size > 1024*1024*0.7:
        raise ValidationError('This file is bigger than 0.7mb')

def validate_size_normal(value):
    if value.file.size > 1024*1024*0.3:
        raise ValidationError('This file is bigger than 0.3mb')

class Homepage(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=60, help_text='Τίτλος Site')
    background_image = models.ImageField(upload_to=upload_background_banner,
                                         validators=[validate_size, ],
                                         help_text='1400px*800px',
                                         blank=True,
                                         null=True,
                                         )
    keywords = models.CharField(max_length=160, blank=True, null=True)
    description = models.CharField(max_length=160, blank=True, null=True)
    circle_image = models.ImageField(upload_to=upload_location,
                                     blank=True,
                                     null=True,
                                     help_text='1920px * 794px',
                                     validators=[validate_size, ]
                                     )
    
    blog_title = models.CharField(max_length=160, blank=True, null=True)
    blog_keywords = models.CharField(max_length=160, blank=True, null=True)
    blog_description = models.CharField(max_length=160, blank=True, null=True)

    store_title = models.CharField(max_length=160, blank=True, null=True)
    store_keywords = models.CharField(max_length=160, blank=True, null=True)
    store_description = models.CharField(max_length=160, blank=True, null=True)

    about_title = models.CharField(max_length=160, blank=True, null=True)
    about_keywords = models.CharField(max_length=160, blank=True, null=True)
    about_description = models.CharField(max_length=160, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = '1. Διαχείριση Αρχικής Σελίδας'

    def __str__(self):
        return self.title

    def tiny_background_image(self):
        return mark_safe("<img src='%s' width='80px' height='50px' >" % self.background_image.url)
    tiny_background_image.short_description = 'Εικόνα background'

    def tiny_circle_image(self):
        return mark_safe("<img src='%s' width='80px' height='50px' >" % self.circle_image.url)
    tiny_circle_image.short_description = 'Εικόνα Δεύτερο background'

class CircleImages(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=150)
    icon = models.CharField(max_length=100, help_text='example fa fa-recycle')
    image = models.ImageField(upload_to=upload_location, help_text='370px*370px', validators=[validate_size_normal, ])
    index_page_related = models.ForeignKey(Homepage, null=True)

    def __str__(self):
        return self.title

class IconMessages(models.Model):
    title = models.CharField(max_length=50)
    icon = models.CharField(max_length=150)
    text = models.CharField(max_length=150, verbose_name="Κείμενο")
    delay = models.IntegerField(default=300, verbose_name="Καθηστέρηση εμφάνισης")
    page_related = models.ForeignKey(Homepage)

    class Meta:
        verbose_name_plural = '3. Δημιουργία Icon μηνυμάτων'

    def __str__(self):
        return self.title

class BannerMessages(models.Model):
    title = models.TextField()
    homepage_related = models.ForeignKey(Homepage, verbose_name='Αρχική Σελίδα', null=True)

    class Meta:
        verbose_name_plural = '4. Δημιουργία μηνυμάτων στο κάτω Banner'

    def __str__(self):
        return self.title


class ContactInfo(models.Model):
    address = models.CharField(max_length=160, verbose_name='Διεύθυνση')
    email = models.EmailField(blank=True, null=True)
    website = models.CharField(max_length=160, blank=True, null=True)
    href = models.URLField(blank=True, null=True, verbose_name='Υπερσύνδεσμος')
    homepage_related = models.ForeignKey(Homepage, verbose_name='Αρχική Σελίδα')

    class Meta:
        verbose_name_plural = '5. Πληροφορίες Καταστημάτος Αρχικής Σελίδας'

    def __str__(self):
        return self.website


class Phones(models.Model):
    title = models.CharField(max_length=10, verbose_name='Τηλέφωνο')
    contact_related = models.ForeignKey(ContactInfo)

    class Meta:
        verbose_name_plural = '6. Τηλέφωνα'

    def __str__(self):
        return self.title


class MainBanner(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=60, verbose_name='Τίτλος', blank=True, null=True)
    image = models.ImageField(upload_to=upload_location, verbose_name='Είκονα', validators=[validate_size_normal, ])
    text = models.TextField(verbose_name='Περιγραφή',blank=True, null=True)
    href = models.URLField(blank=True, null=True, verbose_name='Υπερσύνδεσμος')
    related_page = models.ForeignKey(Homepage, null=True, verbose_name='Αρχική Σελίδα')
    store_related = models.ForeignKey(Store, null=True, verbose_name='Κατάστημα')
    my_query = BannerManager()
    objects = models.Manager()

    class Meta:
        verbose_name_plural = '2. Δημιουργία Banner'

    def __str__(self):
        return '%s %s' %('Banner',self.id)


class InstagramFeed(models.Model):
   instagram_url = models.TextField()
   homepage_related = models.ForeignKey(Homepage)
        