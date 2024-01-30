from django.shortcuts import render
from product.models import Product


def frontpage(request):
    products = Product.objects.all()[0:8]  # This gets the 1st 8 to show on the page from the db
    return render(request, "core/frontpage.html", {"products": products})


def shop(request):
    products = Product.objects.all()

    return render(request, "core/shop.html", {"products": products})
