from django.contrib import admin
from products.models import Category,Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent_category']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'product_category_slug']

    def product_category_slug(self, obj):
        return obj.category.slug
    product_category_slug.admin_order_field  = 'book__author'

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)