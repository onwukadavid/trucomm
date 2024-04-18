from django.shortcuts import render
import requests
from pprint import pprint
import json

categories = [
    "Clothing",
    "Shoes",
    "Watches",
    "Jewellery",
    "Health & Beauty",
    "Sports",
    "Sleepwear",
    "Seasonal Wear",
    "Ethinic Wear",
    "Baby Clothing",
    "Accessories",
    "Men",
    "Women",
    "Kids"
]

def home(request):
    response = requests.get('https://fakestoreapi.com/products')
    if not response.raise_for_status():
        products = response.json()
        category_list = []
        for i in range(len(products)):
            category = products[i]['category']
            if category not in category_list:
                category_list.append(category)
    print(category_list)
    print(len(products))

    return render(request, 'index.html')