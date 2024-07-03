import json
import os
import requests
from pprint import pprint
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.shortcuts import get_list_or_404, render
from django.shortcuts import get_object_or_404
from products.models import Category, Product
from users.models import User

def home(request):
    #TODO: category page and url
    context = {}
    new_arrival = Product.objects.get_new_arrivals().select_related('category')[:8]
    featured = Product.objects.filter(featured=True).select_related('category')[:8]
    special = Product.objects.filter(special=True).select_related('category')[:8]
    context['featured'] = featured
    context['special'] = special
    context['new_arrival'] = new_arrival
    return render(request, 'index.html', context)


def products(request):
    if request.GET and (request.GET != 'page'):
        print(len(request.GET))
        if (len(request.GET)==1) and request.GET.get('new_arrival', False):
            products = Product.objects.get_new_arrivals().select_related('category')
        else:
            filter_params = {}
            for k,v in request.GET.items():
                if k == 'page':
                    continue
                filter_params[k]=v
            products = Product.objects.filter(**filter_params).select_related('category')
    else:
        products = Product.objects.select_related('category').all()

    context = {'products':products}

    paginator = Paginator(products, 3)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    context['page_obj'] = page_obj
     
    return render(request, 'products/products.html', context=context, )


def product_detail(request, category, slug):

    # declare empty context
    context = {}

    # get product from db
    product = get_object_or_404(Product, category__title=category, slug=slug)

    # add product to context
    context['product'] = product

    # return product detail template
    
    return render(request, 'products/product-detail.html', context=context)


def categories(request, slug):

    products = Product.objects.filter(Q(category__slug = slug) | Q(category__title = slug) | Q(category__parent_category__slug = slug)).select_related('category')
    
    paginator = Paginator(products, 3)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    context = {'page_obj':page_obj} 
    return render(request, 'products/products.html', context)   


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
