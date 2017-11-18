from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from products.models import Category
import slugify

@receiver(post_save, sender=Store)
def slug_name(instance, sender, **kwargs):
    if not instance.slug:
        title = slugify.slugify(instance.title)
        slug_exists = Store.objects.filter(slug=title).exists
        instance.slug = '%s' % title
        instance.save()
post_save.connect(slug_name, sender=Store)


@receiver(post_save, sender=Category)
def slug_name(instance, sender, **kwargs):
    if not instance.slug:
        title = slugify.slugify(instance.title)
        slug_exists = Category.objects.filter(slug=title).exists
        instance.slug = '%s' % title
        instance.save()
post_save.connect(slug_name, sender=Category)
