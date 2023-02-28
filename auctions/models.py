from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    class Meta:
        verbose_name        = 'Category'
        verbose_name_plural = 'Categories'

    category_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.category_name}"
    
class Condition(models.Model):
    condition_quality = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.condition_quality}"

class Listing(models.Model):
    title           = models.CharField(max_length=30)
    category        = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    condition       = models.ForeignKey(Condition, null=True, on_delete=models.SET_NULL)
    description     = models.TextField(max_length=300)
    start_dateTime  = models.DateTimeField(auto_now_add=True)
    end_dateTime    = models.DateTimeField(null=True, blank=True)
    seller          = models.ForeignKey(User, on_delete=models.CASCADE)
    starting_price  = models.DecimalField(max_digits=10, decimal_places=2, default=None)

    def __str__(self):
        return f"ID: {self.id}, Title: {self.title}, Description: {self.description}, Listed: {self.start_dateTime}, Ending: {self.end_dateTime}"

    
class Bid(models.Model):
    listing         = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidder          = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    bid_amount      = models.DecimalField(max_digits=10, decimal_places=2)
    bid_dateTime    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bids on {self.listing} are {self.bid_amount} by {self.bidder}, placed at {self.bid_dateTime}"

class Comment(models.Model):
    listing             = models.ForeignKey(Listing, on_delete=models.CASCADE)
    commenter           = models.ForeignKey(User, default=None, null=True, on_delete=models.SET_NULL)
    comment_text        = models.TextField(default="")
    comment_dateTime    = models.DateTimeField(auto_now_add=True)

class Watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user    = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Listing: {self.listing.id}, Title: {self.listing.title}, Watched by {self.user}"