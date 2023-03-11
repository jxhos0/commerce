from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Category, Watchlist, Comment, Bid
from .forms import *

import datetime


def index(request):
    # Run function to check if listings are still active.
    active_check()

    # Check if index link clicked
    if not request.GET: 
        return render(request, "auctions/index.html", {
            "title" : "Active Listings",
            "listings" : Listing.objects.filter(is_active = True).order_by("end_dateTime")
        })
    # Load all active listings page
    else:
        return render(request, "auctions/index.html", {
            "title" : "All Listings",
            "listings" : Listing.objects.all().order_by("-end_dateTime")
        })

@login_required
def create(request):
    # Check for form submission
    if request.method == "POST":
        # Fill form with user entries
        form = NewListingForm(request.POST or None, request.FILES or None)
        
        # Check fields are valid and required fields have data
        if form.is_valid():
            form = form.save(commit=False)      # Save the form data but not to the database yet
            form.seller = request.user          # Enter the current user data into the form
            form.end_dateTime = datetime.datetime.now() + datetime.timedelta(days=int(request.POST.get('auction_duration')))        # Calcualte and enter the auction end date and time
            form.save()                         # Save the form data in database

            # Redirect user to index page
            return HttpResponseRedirect(reverse("index"))
        
        # Return user to create page with error message
        else:
            return render(request, "auctions/create.html", {
                "form" : form
            })      
    # Load create page with empty form
    else:
        return render(request, "auctions/create.html", {
            "form" : NewListingForm()
        })

@login_required
def watchlist(request):
    # Run function to check if listings are still active.
    active_check()

    # Listen to watchlist selector on listing page
    if request.GET.get("watch_listing"):
        # Check if user chooses to add listing
        if "add" in request.GET.get("watch_listing"):
            listing_id = request.GET.get("watch_listing").replace("add ", "")       # Get the listing ID from the watchlist selector
            listing = Listing.objects.get(pk=listing_id)                            # Retrieve listing from the database

            w = Watchlist(listing=listing, user=request.user)                       # Create watchlist entry for the lsiting and user
            w.save()                                                                # Save the watchlist entry

            # Redirect user to the listing page
            return HttpResponseRedirect(reverse("listing", args=[listing_id]))    
        
        # If user wants to remove listing
        else:
            listing_id = request.GET.get("watch_listing").replace("remove ", "")        # Get the listing ID from the watchlist selector
            listing = Listing.objects.get(pk=listing_id)                                # Retrieve listing from the database

            Watchlist.objects.filter(listing=listing).get(user=request.user).delete()   # Remove listing from watchlist of the user

            # Redirect user to the listing page
            return HttpResponseRedirect(reverse("listing", args=[listing_id]))
        
    # Load page with all listings the user is watching
    else:
        return render(request, "auctions/watchlist.html", {
            "watchlist" : Watchlist.objects.filter(user=request.user)
        })
    

def categories(request):
    # Run function to check if listings are still active.
    active_check()
    if request.GET.get("filter"):
        category_filter = request.GET.get("filter")

        filtered_listings = Listing.objects.filter(category = category_filter)

        return render(request, "auctions/categories.html",   {
            "categories"    : Category.objects.all(),
            "listings"      : filtered_listings,
            "selected"      : int(category_filter)
        })
             
    else:
        return render(request, "auctions/categories.html",   {
            "categories"    : Category.objects.all(),
            "listings"      : Listing.objects.all()
        })

def listing(request, id):
    # Run function to check if listings are still active.
    active_check()

    #  Load listing details, bids and comments for the listing
    listing     = Listing.objects.get(pk=id)
    bids        = Bid.objects.filter(listing=id)
    comments    = Comment.objects.filter(listing=id)

    # Check if item has bids, if it does set the required price to the highest bid, else set the required bid as the starting price.
    if bids.count() > 0:
        required_bid = bids.latest('bid_amount').bid_amount
    elif bids.count() == 0:
        required_bid = listing.starting_price

    # Create new bid form and pre-populate with initial data
    bid_form = NewBidForm(initial={"listing" : id, "bidder" : request.user})
    # Modify how bid form will look and set minimum bid requirement
    bid_form.fields['bid_amount'].label = ""
    bid_form.fields['bid_amount'].widget.attrs.update(placeholder="Bid amount", min=required_bid + 1)

    # Create new comment form and pre-populate with initial data
    comment_form = NewCommentForm(initial={"listing" : id, "commenter" : request.user})
    # Modify how comment form will look and set placeholder
    comment_form.fields['comment_text'].label = ""
    comment_form.fields['comment_text'].widget.attrs.update(placeholder="Enter your question here")

    # Try search if item is in users watchlist
    try:
        Watchlist.objects.filter(listing=id).get(user=request.user)

        # Load listing page
        return render(request, "auctions/listing.html", {
            "listing"       : listing,
            "watched"       : True,
            "bids"          : bids,
            "required_bid"  : required_bid,
            "bid_form"      : bid_form,
            "comments"      : comments,
            "comment_form"  : comment_form
        })

    except:
        # Load listing page
        return render(request, "auctions/listing.html", {
            "listing"       : listing,
            "bids"          : bids,
            "required_bid"  : required_bid,
            "bid_form"      : bid_form,
            "comments"      : comments,
            "comment_form"  : comment_form
        })

@login_required
def bid(request, id):
    # Run function to check if listings are still active.
    active_check()

    # Listen for bid submission. 
    if request.method == "POST":
        # Save bid into bid database
        bid_form = NewBidForm(request.POST)
        bid_form.save()

        # Redirect user back to listing
        return HttpResponseRedirect(reverse("listing", args=[id]))

@login_required
def comment(request, id):
    # Run function to check if listings are still active.
    active_check()

    # Listen for bid submission. 
    if request.method == "POST":
        # Save comment into comment database.
        comment_form = NewCommentForm(request.POST)
        comment_form.save()

        # Redirect user back to listing.
        return HttpResponseRedirect(reverse("listing", args=[id]))

@login_required
def close(request, id):
    # Confirm user trying to access the page is the seller
    if request.user == Listing.objects.get(pk=id).seller:
        # Check if action is sleceted via POST
        if request.method == "POST":
            listing = Listing.objects.get(pk=id)        # Retreive listing data
            
            # Check for confirmation user wants to close the listing
            if 'close' in request.POST:
                # Try get the winning bid from bid database
                try:
                    winning_bid = Bid.objects.filter(listing=id).first()

                    # If there is a winning bid, close the listing and set the winner to the bidder with the highest bid.
                    listing.is_active = False
                    listing.winner = winning_bid.bidder
                    listing.save()
                except:
                    # If there is no winner, close the listing with no winner
                    listing.is_active = False
                    listing.save()

                # Redirect user back to listing.
                return HttpResponseRedirect(reverse("listing", args=[id]))
                
            else:
                # Redirect user back to listing.
                return HttpResponseRedirect(reverse("listing", args=[id]))

        # Load the close page  
        else:
            return render(request,"auctions/close.html", {
                "listing" : Listing.objects.get(pk=id)
            })
    
    # Redirect to index page if user isn't the seller
    else:
        return HttpResponseRedirect(reverse("index"))
    
def active_check():
    # Load all listing that are currently active
    listings = Listing.objects.filter(is_active = True)

    # Loop through listings and check the end date has been passed 
    for listing in listings:
        if listing.end_dateTime <= timezone.now():
            # Try get the winning bid from bid database
            try:
                winning_bid = Bid.objects.filter(listing=id).first()

                # If there is a winning bid, close the listing and set the winner to the bidder with the highest bid.
                listing.is_active = False
                listing.winner = winning_bid.bidder
                listing.save()
            except:
                # If there is no winner, close the listing with no winner
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
