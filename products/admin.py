from django.contrib import admin
from products.models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent_category']

# Register your models here.
admin.site.register(Category, CategoryAdmin)