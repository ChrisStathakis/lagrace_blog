from django.db.models.signals import post_save
from django.dispatch import receiver
import slugify
from .models import *



@receiver(post_save, sender=BlogCategory)
def create_blog_category_slug(sender, instance,**kwargs):
    if not instance.slug:
        title = slugify.slugify(instance.title)
        slug_exists = BlogCategory.objects.filter(slug=title).exists
        instance.slug = '%s' % title
        instance.save()


@receiver(post_save, sender=Post)
def create_post_slug(sender, instance,**kwargs):
    get_category = instance.category.title if instance.category else 'No category'
    if not instance.slug:
        title = slugify.slugify(instance.title)
        slug_exists = Post.objects.filter(slug=title).exists
        instance.slug = '%s' % title
        instance.save()
    get_brands = Brands.objects.filter(post_related=instance)
    
    if not instance.keywords:
        new_keywords = ['Lagrece', 'Μολάοι', 'Σκάλα', 'Καταστήματα']
        new_keywords.append(instance.title)
        new_keywords.append(get_category)
        if get_brands:
            for brand in get_brands:
                new_keywords.append(brand.title)
        instance.keywords = ', '.join(new_keywords)
        instance.save()
    if not instance.meta_description:
        instance.meta_description = 'Τα Καταστήματα LaGrace σας καλοσωρίζουν στο blog με θέμα %s στην κατηγορία %s' % (instance.title, get_category)
        instance.save()




@receiver(post_save, sender=Brands)
def create_brands_slug(sender, instance,**kwargs):
    if not instance.slug:
        title = slugify.slugify(instance.title)
        slug_exists = Brands.objects.filter(slug=title).exists
        instance.slug = '%s' % title
        instance.save()





@receiver(post_save, sender=Gallery)
def create_gallery_title(sender, instance,**kwargs):
    if not instance.title:
        instance.title = '%s %s' % (instance.post_related.title, instance.id)
        instance.save()