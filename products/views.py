from django.shortcuts import render
from products.models import Category
import requests
from pprint import pprint
import json
from django.http import JsonResponse

# def home(request):
#     response = requests.get('https://fakestoreapi.com/products')
#     if not response.raise_for_status():
#         products = response.json()
#         category_list = []
#         for i in range(len(products)):
#             category = products[i]['category']
#             if category not in category_list:
#                 category_list.append(category)
#     print(category_list)
#     print(len(products))

#     return render(request, 'index-2.html')

def home(request):
    context = {}
    categories = Category.objects.filter(parent_category=None)

    context['categories'] = categories[:4]

    return render(request, 'index.html', context=context)


def populate_categories(request):
    # categories = Category.objects.all()
    # print(categories)

    json_data = open('D:\\Users\\Truman-david\\Desktop\\django-projects\\TruComm\\trucomm\\products\\categories.json')

    # Load JSON data
    categories_data = json.loads(json_data.read)

    # Function to recursively create categories and subcategories
    def create_categories(data, parent=None):
        for category_data in data:
            category_obj = Category.objects.create(
                title=category_data['title'],
                slug=category_data['slug'],
                parent_category=parent
            )
            if 'subcategories' in category_data:
                create_categories(category_data['subcategories'], parent=category_obj)

    # Call the function to populate categories
    create_categories(categories_data)

    return render(request, 'index-2.html')