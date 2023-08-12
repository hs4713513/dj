from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name=models.CharField( max_length=50 )
    
class Bid(models.Model):
    bid=models.DecimalField(max_digits=4,decimal_places=2)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user")

class Listing(models.Model):
    title=models.CharField(max_length=50)
    desc=models.CharField(max_length=50 ,default=None,blank=True)
    is_close=models.BooleanField(default=False)
    url=models.CharField(max_length=300)
    owner=models.ForeignKey(User,on_delete=models.CASCADE, related_name="listings")
    watchlist=models.ManyToManyField(User,related_name="watchlist")
    price=models.ForeignKey(Bid, on_delete=models.CASCADE,related_name="b",default=5)
    
class Comments(models.Model):
    text=models.TextField()
    writer=models.ForeignKey(User,on_delete=models.CASCADE,related_name="comment")
    listing=models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="comm")
    

    

    
    
    

