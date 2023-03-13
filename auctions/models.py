from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    class Meta:
        verbose_name        = 'Category'
        verbose_name_plural = 'Categories'

    category_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.category_name}"
    
class Condition(models.Model):
    condition_quality = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.condition_quality}"

class Listing(models.Model):
    title           = models.CharField(max_length=30)
    category        = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    condition       = models.ForeignKey(Condition, blank=True, null=True, on_delete=models.SET_NULL)
    description     = models.TextField(max_length=300)
    image           = models.URLField(blank = True, null=True)
    start_dateTime  = models.DateTimeField(auto_now_add=True)
    end_dateTime    = models.DateTimeField(null=True, blank=True)
    seller          = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    starting_price  = models.DecimalField(max_digits=10, decimal_places=2, default=None)
    is_active       = models.BooleanField(default=True)
    winner          = models.ForeignKey(User, blank=True, default=None, null=True, on_delete=models.SET_NULL, related_name="winner")

    def __str__(self):
        if self.is_active:
            return f"{self.title}, sold by {self.seller} ends {self.end_dateTime.strftime('%d-%m-%Y %I:%M %p')}"
        else:
            if self.winner:
                return f"{self.title}, sold by {self.seller} ended {self.end_dateTime.strftime('%d-%m-%Y %I:%M %p')} and was won by {self.winner}"
            else:
                return f"{self.title}, sold by {self.seller} ended {self.end_dateTime.strftime('%d-%m-%Y %I:%M %p')}"
        
class Bid(models.Model):
    listing         = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidder          = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    bid_amount      = models.DecimalField(max_digits=10, decimal_places=2)
    bid_dateTime    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder} bidded ${self.bid_amount} on listing '{self.listing.title}', at {self.bid_dateTime.strftime('%d-%m-%Y %I:%M %p')}"

class Comment(models.Model):
    listing             = models.ForeignKey(Listing, on_delete=models.CASCADE)
    commenter           = models.ForeignKey(User, default=None, null=True, on_delete=models.SET_NULL)
    comment_text        = models.TextField(default="")
    comment_dateTime    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.commenter} commented on listing '{self.listing.title}' at {self.comment_dateTime.strftime('%d-%m-%Y %I:%M %p')} "

class Watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user    = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Listing '{self.listing.title}', is being watched by {self.user}"