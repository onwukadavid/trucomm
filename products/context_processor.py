from django.contrib.auth.decorators import login_required
from products.models import Category, Product


def categories_processor(request):
    categories_list = Category.objects.filter(parent_category=None).values('id', 'title')[:4]
    categories_id = [categories['id'] for categories in categories_list]
    categories_title = [categories['title'] for categories in categories_list]

    subcategories_list = Category.objects.filter(parent_category__in=categories_id).values('parent_category_id__title','title')

    categories = {}
    for category in categories_title:
        categories.setdefault(category, [])
        categories[category] += [new_subcat['title'] for new_subcat in subcategories_list if new_subcat['parent_category_id__title'] == category]

    return {'categories':categories}