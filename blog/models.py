from django.db import models
from django.core.exceptions import ValidationError
from tinymce.models import HTMLField
from django.utils.safestring import mark_safe
from django.urls import reverse
# Create your models here.


def upload_to_blog(instance, filename):
	return 'blog/%s/%s' % (instance.title, filename)

def upload_to_blog_gal(instance, filename):
	return 'blog_gallery/%s/%s' % (instance.post_related.title, filename)

def upload_to_blog_cat(instance, filename):
	return 'blog_cat/%s/%s' % (instance.title, filename)

def validate_size(value):
	if value.file.size > 1024*1024:
		return ValidationError('This is bigger than 1mb.')

class BlogCategory(models.Model):
	active = models.BooleanField(default=True)
	title = models.CharField(unique=True, max_length=150)
	slug = models.SlugField(blank=True, null=True, allow_unicode=True)
	css_class = models.CharField(blank=True, null=True, max_length=10)
	image = models.ImageField(upload_to=upload_to_blog_cat, validators=[validate_size, ], null=True, help_text='1360px*440px')
	carousel_image = models.ImageField(upload_to=upload_to_blog_cat, validators=[validate_size, ], null=True, help_text='1360px*440px')
	
	class Meta:
		ordering = ['title']
		
	def __str__(self):
		return self.title

	def tiny_tag_image(self):
		return mark_safe("<img src='%s' width='100px' height='50px' >" % self.image.url)

	def tiny_tag_carousel_image(self):
		return mark_safe("<img src='%s' width='100px' height='50px' >" % self.carousel_image.url)


class PostManager(models.Manager):

	def active_posts(self):
		return super(PostManager, self).filter(active=True)

class Post(models.Model):
	active = models.BooleanField(default=True)
	featured = models.BooleanField(default=False)
	title = models.CharField(unique=True, max_length=150)
	slug = models.SlugField(blank=True, null=True, allow_unicode=True)
	image = models.ImageField(upload_to=upload_to_blog, validators=[validate_size, ])
	keywords = models.CharField(max_length=150, blank=True, null=True)
	meta_description = models.CharField(max_length=150, blank=True, null=True)
	category = models.ForeignKey(BlogCategory, null=True)
	context = HTMLField(blank=True, null=True)
	date_added = models.DateTimeField(auto_now_add=True)
	date_edited = models.DateTimeField(auto_now=True)
	my_query = PostManager()
	objects = models.Manager()

	class Meta:
		ordering = ['-featured', '-date_added']

			
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog_detail', kwargs={'slug':self.slug})

	def tiny_image(self):
		return mark_safe("<img src='%s' width='100px' height='100px' >" % self.image.url)





class Brands(models.Model):
	active = models.BooleanField(default=True)
	title = models.CharField(unique=True, max_length=150)
	slug = models.SlugField(blank=True, null=True, allow_unicode=True)
	image = models.ImageField(upload_to=upload_to_blog, validators=[validate_size, ],)
	keywords = models.CharField(max_length=150, blank=True, null=True)
	meta_description = models.CharField(max_length=150, blank=True, null=True)
	context = HTMLField(blank=True, null=True)
	date_added = models.DateTimeField(auto_now_add=True)
	date_edited = models.DateTimeField(auto_now=True)
	post_related = models.ManyToManyField(Post, blank=True, null=True)
	css_class = models.CharField(unique=True, max_length=10, null=True)
	href = models.URLField(blank=True, null=True)

	class Meta:
		ordering=['title', ]

	def __str__(self):
		return self.title

	def tiny_tag_image(self):
		return mark_safe("<img src='%s' width='50px' height='50px' >" % self.image.url)


		

class Gallery(models.Model):
	active = models.BooleanField(default=True)
	title = models.CharField(max_length=150, blank=True, null=True)
	image = models.ImageField(upload_to=upload_to_blog_gal, validators=[])
	alt = models.CharField(max_length=150, blank=True, null=True)
	date_added = models.DateTimeField(auto_now_add=True)
	date_edited = models.DateTimeField(auto_now=True)
	post_related = models.ForeignKey(Post, )
	brand_related = models.ForeignKey(Brands, null=True, blank=True)
	href = models.URLField(blank=True, null=True)

	def tiny_tag_image(self):
		return mark_safe("<img src='%s' width='100px' height='100px' >" % self.image.url)

	def __str__(self):
		return '%s-%s' % ('gallery', self.id)

	def href_(self):
		if self.href:
			return self.href
		return self.brand_related.href if self.brand_related.href else None

	


