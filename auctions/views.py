from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from .models import User, Listing, Category
from .forms import NewListingForm

import datetime


def index(request):
    return render(request, "auctions/index.html", {
        "listings" : Listing.objects.all()
    })

def create(request):
    if request.method == "POST":
        
        form = NewListingForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            form = form.save(commit=False)
            form.seller = request.user
            form.end_dateTime = datetime.datetime.now() + datetime.timedelta(days=int(request.POST.get('auction_duration')))
            form.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {
                "form" : form
            })      
    
    else:
        return render(request, "auctions/create.html", {
            "form" : NewListingForm()
        })

def watchlist(request):
    return render(request, "auctions/watchlist.html")

def categories(request):
    if request.GET.get("filter"):
        category_filter = request.GET.get("filter")

        print(category_filter)

        filtered_listings = Listing.objects.filter(category = category_filter)

        return render(request, "auctions/categories.html",   {
            "categories" : Category.objects.all(),
            "listings" : filtered_listings
        })
             
    
    else:
        print("no filter")
        return render(request, "auctions/categories.html",   {
            "categories" : Category.objects.all(),
            "listings" : Listing.objects.all()
        })

def listing(request, id):
    return render(request, "auctions/listing.html", {
        "id" : id
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
