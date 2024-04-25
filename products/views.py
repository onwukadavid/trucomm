from django.shortcuts import render
from products.models import Category, Product
import requests
from pprint import pprint
import json
from django.http import HttpResponse, JsonResponse
import os

def home(request):
    context = {}
    categories = Category.objects.filter(parent_category=None)

    context['categories'] = categories[:4]

    return render(request, 'index.html', context=context)


def products(request):
    products = Product.objects.all()

    context = {'products':products}
     
    return render(request, 'products.html', context=context)


def populate_categories(request):
    json_data = open('D:\\Users\\Truman-david\\Desktop\\django-projects\\TruComm\\trucomm\\products\\categories2.json')

    # Load JSON data
    categories_data = json.loads(json_data.read())

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

    return HttpResponse('Hello')


def populate_products(request):
    categories = [category.title for category in Category.objects.all()]
    categories2 = ["mens-watches","womens-watches","sunglasses"]

    # url = "https://apidojo-hm-hennes-mauritz-v1.p.rapidapi.com/products/list"
    url = "https://dummyjson.com/products//category/womens-shoes"

    querystring = {"country":"us","lang":"en","currentpage":"0","pagesize":"30","categories":"men_all","concepts":"H&M MAN"}

    headers = {
	"X-RapidAPI-Key": os.environ.get('X_RapidAPI_Key'),
	"X-RapidAPI-Host": os.environ.get('X_RapidAPI_Host')
    }

    # response = requests.get(url, headers=headers, params=querystring).json()
    response = requests.get(url).json()
    # return JsonResponse(response['products'])

    products = response['products']
    # print(len(products))

    for product in products:
        # if product['category'] in categories2:
            product_title = product['title']
            description =  "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus maximus dolor at ante bibendum dignissim. \
                            Duis pellentesque vitae massa ac tempor. Vivamus ac urna sed sem faucibus tempus. Cras ut magna malesuada, fermentum ipsum ac, auctor neque. \
                            Nullam congue ligula ligula, non ornare dolor imperdiet at. "
            price = product['price']
            image = product['images'][0]
            # category = product['categoryName']

            Product.objects.create(
                title=product_title,
                description=description,
                price=price,
                image=image,
                category=Category.objects.get(slug='women-shoes')
            )

    return HttpResponse('Hello')
    # return JsonResponse(response.json())
