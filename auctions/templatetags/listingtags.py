# Tutorial at https://realpython.com/django-template-custom-tags-filters/#using-django-templates


from django import template
from ..models import User, Listing, Category, Watchlist, Comment, Bid

from django.utils import timezone

register = template.Library()

@register.filter
def bid_count(listing):
    bids = Bid.objects.filter(listing=listing.id)
    bid_count = len(bids)
    if bid_count == 1:
        return f"{ bid_count } bid"
    else:
        return f"{ bid_count } bids" 

@register.filter  
def timeremaining(listing):
    end_time = Listing.objects.get(pk=listing.id).end_dateTime
    
    td = end_time - timezone.now()
    td_hrs = td.seconds//3600%60
    td_mins = (td.seconds//60)%60

    if td.days > 0:
        return f"{ td.days }d { td_hrs }h"
    else:
        if td_hrs > 0:
            return f"{ td_hrs }h { td_mins }m" 
        else:
            return f"{ td_mins }m { td.seconds % 60 }s"


@register.filter  
def format_endDateTime(listing):
    end_time = Listing.objects.get(pk=listing.id).end_dateTime

    td = end_time - timezone.now()

    if td.days == 0:
        return f"Today { end_time.strftime('%H:%M') }"
    elif td.days == 1:
        return f"Tomorrow { end_time.strftime('%H:%M') }"
    else:
        return f"{ end_time.strftime('%d/%m %H:%M') }"

@register.filter
def current_price(listing):
    bids = Bid.objects.filter(listing=listing.id)

    if bids.count() > 0:
        price = bids.latest('bid_amount').bid_amount
    elif bids.count() == 0:
        price = listing.starting_price

    return price