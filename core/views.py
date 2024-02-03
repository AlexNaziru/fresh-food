from django.shortcuts import render
from product.models import Product, Category
from django.db.models import Q


def frontpage(request):
    products = Product.objects.all()[0:8]  # This gets the 1st 8 to show on the page from the db
    return render(request, "core/frontpage.html", {"products": products})

def signup(request):
    return render(request, "core/signup.html")

def shop(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    active_category = request.GET.get("category", "")
    # Filtering categories
    if active_category:
        products = products.filter(category__slug=active_category)

    # Search option
    query = request.GET.get("query", '')  # Defaults to empty
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
         # Incontains bc we don't want to be case-sensitive and searching description also

    context = {
        "categories": categories,
        "products": products,
        "active_category": active_category
    }

    return render(request, "core/shop.html", context)
