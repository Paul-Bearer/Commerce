from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):
    title = models.CharField(max_length=25)
    description = models.CharField(max_length=500)
    starting_price = models.IntegerField()
    photo = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_owner")
    category = models.CharField(max_length=25)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_owner")
    amount = models.IntegerField()
    item = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bidded_item")
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item}---${self.amount}"   

class Comment(models.Model):
    item = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="comment_item")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_owner")
    comment = models.CharField(max_length=250)
    date_time = models.DateTimeField(auto_now_add=True)

class Watchlist(models.Model):
    item = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="watchlist_item")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_owner") 
    


