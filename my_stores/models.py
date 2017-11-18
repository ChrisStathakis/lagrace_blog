from django.db import models
from django.utils.safestring import mark_safe
from django.urls import reverse
# Create your models here.

MEDIA = 'https://lagracemol.s3.amazonaws.com/media/'

def upload_location(instance, filename):
    return 'store_gallery/%s/%s' % (instance.store_related.title, filename)

def validate_size(value):
    if value.file.size > 1024*1024*0.3:
        return ValidationError('The file is bigger than 0.3mb')

class Store(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(unique=True, max_length=60)
    text = models.TextField(blank=True, null=True, verbose_name='Κείμενο')
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)
    address = models.TextField(blank=True, null=True, verbose_name='Διεύθυνση')
    latitude = models.DecimalField(default=36.803335, max_digits=8, decimal_places=6, verbose_name='Google map latitude')
    longitude = models.DecimalField(default=22.851774, max_digits=8, decimal_places=6, verbose_name='Google map longitude')
    
    class Meta:
        verbose_name_plural = '1. Διαχείριση Καταστημάτων'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('store_detail', kwargs={'slug':self.slug})

    @property    
    def image(self):
        image_qs = StoreGallery.objects.filter(active=True, store_related=self, main_image=True)
        return StoreGallery.objects.filter(active=True, main_image=True, store_related=self).last().image if image_qs else None

    def all_images(self):
        return StoreGallery.objects.filter(active=True, store_related=self).exclude(main_image=True)

class StorePhone(models.Model):
    title = models.CharField(max_length=10)
    store_related = models.ForeignKey(Store, verbose_name='Κατάστημα')

    class Meta:
        verbose_name_plural = '5. Τηλέφωνα Καταστημάτων'

    def __str__(self):
        return self.title




class StoreGallery(models.Model):
    active= models.BooleanField(default=True)
    title = models.CharField(max_length=60 ,blank=True, null=True)
    image = models.ImageField(upload_to=upload_location, validators=[validate_size, ])
    store_related = models.ForeignKey(Store)
    alt = models.CharField(max_length=30, blank=True, null=True)
    main_image = models.BooleanField(default=False)


    class Meta:
        verbose_name_plural = '2. Gallery Καταστημάτων'

    def __str__(self):
        return '%s %s' % (self.store_related.title, self.id)

    def tiny_image_tag(self):
        return mark_safe("<img src='%s' width='200px' height='100px' " %  self.image.url)




class StoreWork(models.Model):
    title = models.CharField(max_length=30)
    time_start = models.CharField(max_length=10)
    time_end = models.CharField(max_length=10)
    store_related = models.ManyToManyField(Store,  verbose_name='Κατάστημα')

    class Meta:
        verbose_name_plural = '6. Ωράριο Καταστημάτων'

    def __str__(self):
        return self.title

class StoreServices(models.Model):
    title = models.CharField(max_length=60)
    text = models.CharField(max_length=60)
    icon = models.CharField(max_length=100, help_text='fa fa-user')
    page_related = models.ForeignKey(Store, null=True)

    class Meta:
        verbose_name_plural = '4. Services Καταστημάτων'

    def __str__(self):
        return self.title