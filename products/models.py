from django.db import models
from django.template.defaultfilters import slugify
from cloudinary.models import CloudinaryField
from products.managers import CategoryManager, ProductManager
from django.utils import timezone

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    parent_category = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True, related_name='subcategories')
    is_visible = models.BooleanField(default=False)


    # objects = CategoryManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'category'
        verbose_name_plural = 'categories'
        constraints = [
            models.UniqueConstraint('title', 'parent_category', name='unique_category')
        ]

    def __str__(self):
        return self.title


class Product(models.Model):
    title =  models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    # image = models.ImageField('products') # use ImageField For production
    image = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='category')
    season = models.CharField(max_length=255, default='', blank=True, null=True)
    special = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    # tags = models.
    created_at = models.DateTimeField(verbose_name='created at', default=timezone.now)
    updated_at = models.DateTimeField(verbose_name='updated at', auto_now=True)

    objects = ProductManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.title
    
    def new_arrival(self):
        future = self.created_at+timezone.timedelta(1)
        return timezone.now() <= future