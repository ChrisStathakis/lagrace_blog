from django.db import models
from my_stores.models import Store
from products.models import *
from django.utils.safestring import mark_safe

# Create your models here.
MEDIA = 'media'
CURRENCY = '€'

def product_upload_image(instance, filename):
    return 'products/%s/%s' % (instance.product_related.title, filename)

def category_upload(instance, filename):
    return 'category/%s/%s' % (instance.title, filename)

class ProductsManager(models.Manager):
    def homepage_products(self):
        return super(ProductsManager, self).filter(active=True, first_page=True)[:20]
    def active_products(self):
        return super(ProductsManager, self).filter(active=True)


class Brand(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=60)
    href = models.URLField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    class Meta:
        verbose_name_plural = '3. Διαχείριση Brand'
        ordering = ['title']

    def __str__(self):
        return self.title


class Category(models.Model):
    active = models.BooleanField(default=True)
    first_page = models.BooleanField(default=True)
    image = models.ImageField(null=True, upload_to=category_upload)
    title = models.CharField(max_length=60)
    href = models.URLField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)
    text = models.TextField(null=True, blank=True, default='<span> Από..</span> 30.00 €')
    brands_related = models.ManyToManyField(Brand)

    class Meta:
        verbose_name_plural = '2. Διαχείριση Κατηγορίας'
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('category_page', kwargs={'slug':self.slug})

    def __str__(self):
        return self.title

    def count_items(self):
        counting = Product.objects.filter(active=True, category=self).exists()
        if counting:
            return True
        return False

class ProductsManager(models.Manager):

    def homepage_products(self):
        return super(ProductsManager, self).filter(active=True, first_page=True)[:20]

    def active_products(self):
        return super(ProductsManager, self).filter(active=True)

    def active_products_category(self, category):
        return self.active_products().filter(category=category)

    def featured(self):
        return self.active_products().filter(featured=True)

    def featured_products_by_category(self, category):
        return self.featured().filter(category=category)

    def popular(self):
        return self.active_products().filter(popular=True)[:8]

class Product(models.Model):
    active = models.BooleanField(default=True)
    first_page = models.BooleanField(default=False, verbose_name='Εμφάνιση στην Αρχική Σελίδα')
    popular = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    title = models.CharField(max_length=300, verbose_name='Τίτλος')
    text = models.TextField(blank=True, null=True, verbose_name='Περιγραφή')
    image_href = models.URLField(blank=True, null=True, verbose_name='Link Εικόνας Mymoda.gr')
    brand = models.ForeignKey(Brand, blank=True, null=True)
    category = models.ForeignKey(Category, blank=True, null=True)
    my_moda = models.URLField(blank=True, null=True, verbose_name='Link στο Mymoda.gr')
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2, verbose_name='Αρχική Τιμή')
    price_discount = models.DecimalField(default=0, max_digits=6, decimal_places=2, blank=True, verbose_name='Τιμή Έκπτωσης')
    store_related = models.ManyToManyField(Store)
    slug = models.SlugField(blank=True, null=True)
    my_query = ProductsManager()
    objects = models.Manager()

    class Meta:
        verbose_name_plural = '1. Διαχείριση Προϊόντων'
        ordering = ['title']

    def __str__(self):
        return self.title

    def image(self):
        image_exists = ProductGallery.objects.filter(product_related=self)
        if self.image_href:
            return self.image_href
        if image_exists:
            return image_exists.last().image
        return None

    def tag_active(self):
        if self.active:
            return mark_safe("<td class='table-success'>Ενεργό </td>")
        return mark_safe("<td class='table-danger'>Ανενεργό </td>" )

    def tag_first_page(self):
        if self.first_page:
            return mark_safe("<td class='table-success'>Ενεργό </td>")
        return mark_safe("<td class='table-danger'>Ανενεργό </td>" )

    def tag_price(self):
        if self.price_discount > 0:
            return "%s %s από <del style='color:red;'>%s</del> %s" % (self.price_discount, CURRENCY, self.price, CURRENCY)
        return '%s %s' % (self.price, CURRENCY)

    def tiny_image_tag(self):
        image_url = self.image_href
        get_image = ProductGallery.objects.filter(main_photo=True, active=True, product_related=self).last()
        if get_image:
            image_url = get_image.image.url
        return mark_safe("<img src='%s' width='100px' height='100px' >" % image_url)

class CategoryServices(models.Model):
    title = models.CharField(max_length=60)
    text = models.CharField(max_length=60)
    icon = models.CharField(max_length=100, help_text='fa fa-user')
    page_related = models.ForeignKey(Category, null=True)

    class Meta:
        verbose_name_plural = '4. Services Κατηγοριών'

    def __str__(self):
        return self.title


class ProductGallery(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=60, blank=True, null=True)
    image = models.ImageField(upload_to=product_upload_image)
    product_related = models.ForeignKey(Product)
    main_photo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = '4. Gallery Photo Προϊόντων'

    def __str__(self):
        return self.product_related.title

    def image_admin(self):
        if self.image:
            return mark_safe('<img src="/directory/%s" width="150" height="150" />' % (self.image))
    image_admin.short_description = 'Thumb'
