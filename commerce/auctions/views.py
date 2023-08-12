from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Listing,Bid,Comments
from decimal import Decimal
from django.contrib import messages

from .models import User


def index(request):
    listing=Listing.objects.all()
    return render(request, "auctions/index.html",{'listing':listing})
def display(request,list_id):
    list=Listing.objects.get(pk=list_id)
    comments=list.comm.all()
    context={'list':list,
                 'comments':comments,
    }
    
    return render(request,"auctions/listing_page.html",context)

def add(request,list_id):
    user=request.user
    print("hello")
    list=Listing.objects.get(pk=list_id)
    if list.watchlist.filter(pk=user.pk).exists():
        print("hello")
        list.watchlist.remove(user)
    else:
        list.watchlist.add(user)
    return HttpResponseRedirect(reverse("display",args=(list_id,)))

def create(request):
    if request.method=="POST":
        title=request.POST['title']
        desc=request.POST['desc']
        url=request.POST['url']
        price=request.POST['price']
        user=request.user
        bid=Bid(bid=price,user=user)
        bid.save()
        list=Listing(title=title,desc=desc,url=url,price=bid,owner=user)
        list.save()
        return HttpResponseRedirect(reverse("index"))
    
    else:
        return render(request,"auctions/createlist.html")

def displaywatch(request):
    user=request.user
    list=user.watchlist.all()
    return render(request,"auctions/display.html",{'lists':list})
    

def newbid(request,list_id):
    if request.method=="POST":
        list=Listing.objects.get(pk=list_id)
        currentbid=list.price.bid
        #print(currentbid+2)
        newbid=Decimal(request.POST['bid'])
        if newbid>currentbid:
            updatebid=Bid(bid=newbid,user=request.user)
            print("hello")
            updatebid.save()
            list.price=updatebid
            list.save()
            message="you have successfully placed bid and your bid is highest"
            
            context={
                "list":list,
                "message":message
            }
            messages.success(request,message)
            
            return render(request,"auctions/listing_page.html",context)
    
        else:
            return HttpResponse("not submitted")
        
def addcomments(request,list_id):
    if request.method=="POST":
        
        list=Listing.objects.get(pk=list_id)
        user=request.user
        text=request.POST['comment']
        comment=Comments(text=text,writer=user,listing=list)
        comment.save()
        
        
        return HttpResponseRedirect(reverse("display",args=(list.id,)))
    
def closea(request,list_id):
    list=Listing.objects.get(pk=list_id)
    list.is_close=True
    list.save()
    return HttpResponseRedirect(reverse("display",args=(list_id,)))

    
        
    
    
    
    


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
