from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from product.models import Product, Category
from django.db.models import Q
from .forms import SignUpForm


def frontpage(request):
    products = Product.objects.all()[0:8]  # This gets the 1st 8 to show on the page from the db
    return render(request, "core/frontpage.html", {"products": products})


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("/")
    else:
        form = SignUpForm()
    return render(request, "core/signup.html", {"form": form})


@login_required
def myaccount(request):

    return render(request, "core/myaccount.html")


@login_required
def edit_myaccount(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.save()

        return redirect("myaccount")
    return render(request, "core/edit_myaccount.html")


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
