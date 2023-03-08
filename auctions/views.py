from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal



from .models import User, Listing, Category, Watchlist, Comment, Bid
from .forms import *

import datetime


def index(request):
    active_check()
    return render(request, "auctions/index.html", {
        "listings" : Listing.objects.filter(is_active = True).order_by("end_dateTime")
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
    if request.GET.get("watch_listing"):
        if "add" in request.GET.get("watch_listing"):
            listing_id = request.GET.get("watch_listing").replace("add ", "")

            listing = Listing.objects.get(pk=listing_id)

            w = Watchlist(listing=listing, user=request.user)
            w.save()
            return HttpResponseRedirect(reverse("listing", args=listing_id))
        
        else:
            listing_id = request.GET.get("watch_listing").replace("remove ", "")
            listing = Listing.objects.get(pk=listing_id)

            Watchlist.objects.filter(listing=listing).get(user=request.user).delete()

            return HttpResponseRedirect(reverse("listing", args=listing_id))
    
    else:
        return render(request, "auctions/watchlist.html", {
            "watchlist" : Watchlist.objects.filter(user=request.user)
        })
    

def categories(request):
    if request.GET.get("filter"):
        category_filter = request.GET.get("filter")

        filtered_listings = Listing.objects.filter(category = category_filter)

        return render(request, "auctions/categories.html",   {
            "categories"    : Category.objects.all(),
            "listings"      : filtered_listings
        })
             
    else:
        return render(request, "auctions/categories.html",   {
            "categories"    : Category.objects.all(),
            "listings"      : Listing.objects.all()
        })

def listing(request, id):

    listing = Listing.objects.get(pk=id)
    bids = Bid.objects.filter(listing=id)
    comments = Comment.objects.filter(listing=id)

    if bids.count() > 0:
        required_bid = bids.latest('bid_amount').bid_amount
    elif bids.count() == 0:
        required_bid = listing.starting_price

    initial_bid_data = {
        "listing" : id,
        "bidder" : request.user
    }

    bid_form = NewBidForm(initial=initial_bid_data)

    bid_form.fields['bid_amount'].label = ""
    bid_form.fields['bid_amount'].widget.attrs.update(placeholder="Bid amount", min=required_bid+Decimal(0.01))

    initial_comment_data = {
        "listing" : id,
        "commenter" : request.user
    }

    comment_form = NewCommentForm(initial=initial_comment_data)
    comment_form.fields['comment_text'].label = ""
    comment_form.fields['comment_text'].widget.attrs.update(placeholder="Enter your question here")

    try :
        Watchlist.objects.filter(listing=id).get(user=request.user)

        return render(request, "auctions/listing.html", {
            "listing"   : listing,
            "watched"   : True,
            "bids"      : bids,
            "required_bid" : required_bid,
            "bid_form" : bid_form,
            "comments"  : comments,
            "comment_form" : comment_form
        })

    except:
        return render(request, "auctions/listing.html", {
            "listing"   : listing,
            "bids"      : bids,
            "required_bid" : required_bid,
            "bid_form" : bid_form,
            "comments"  : comments,
            "comment_form" : comment_form
        })

def bid(request):
    if request.method == "POST":
        bid_form = NewBidForm(request.POST)
        bid_form.save()
    return HttpResponseRedirect(reverse("index"))

def comment(request):
    if request.method == "POST":
        comment_form = NewCommentForm(request.POST)
        comment_form.save()
        return HttpResponseRedirect(reverse("index"))

def close(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=id)

        if 'close' in request.POST:
            listing.is_active = False
            listing.save()

            return HttpResponseRedirect(reverse("index"))
            
        else:
            return HttpResponseRedirect(reverse("index"))
            
    else:
        return render(request,"auctions/close.html", {
            "listing" : Listing.objects.get(pk=id)
        })

def active_check():
    listings = Listing.objects.filter(is_active = True)

    for listing in listings:
        if not listing.end_dateTime >= timezone.now():
            listing.is_active = False
            listing.save()
    

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
