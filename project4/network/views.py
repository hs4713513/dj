from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import posts,Like
import json

from .models import User


        
    
    
    
    
def index(request):
    if request.method=="POST":
        user=request.user
        content=request.POST['content']
        if content!="":
            post=posts.objects.create(title=user,content=content,timestamp=datetime.datetime.today())
            post.save()
        
        poste=posts.objects.all().order_by('-timestamp')
        return render(request,"network/index.html",{'posts':poste})
    else:
        poste=posts.objects.all().order_by('-timestamp')
        return render(request,"network/index.html",{'posts':poste})
        


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
    
    
#.............................................................................
@csrf_exempt
@login_required  
def edit(request,post_id):
    p=posts.objects.get(id=post_id)
    if request.method=="PUT":
        data=json.loads(request.body)
        if data.get("post") is not None:
            p.content=data["post"]
        p.save()
        return HttpResponse(status=204)
            
        
@csrf_exempt
@login_required       
def like(request,post_id):
    p=posts.objects.get(id=post_id)
    if request.method=="GET":
        return JsonResponse(p.serialise())
    if request.method=="PUT":
        data=json.loads(request.body)
        if data.get("like"):
            user=request.user
            like=Like.objects.create(post=p,user=user)
            like.save()
            p.likes=Like.objects.filter(post=p).count()
        p.save()
        return HttpResponse(status=204)
    