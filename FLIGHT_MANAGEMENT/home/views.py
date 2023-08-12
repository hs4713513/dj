from django.shortcuts import render,HttpResponse
from home.models import Flight,Airport,Passenger
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
     if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
     else:
          
         return render(request,"home/index.html",{"flights":Flight.objects.all()})


def flight(request,flight_id):
     flight=Flight.objects.get(id=flight_id)
     passenger=flight.passengers.all()
     non_passengers = Passenger.objects.exclude(flights=flight).all()
     return render(request,'home/flight.html',{"flight":flight,"passengers":passenger,"non_passengers":non_passengers})
     

def book(request,flight_id):
     if request.method=="POST":
          flight=Flight.objects.get(pk=flight_id)
          passenger_id=int(request.POST["passenger"])
          passenger=Passenger.objects.get(pk=passenger_id)
          passenger.flights.add(flight)
          return HttpResponseRedirect(reverse("flight",args=[flight.id]))

def login_view(request):
     if request.method=="POST":
          username=request.POST['name']
          password=request.POST['pass']
          myuser=authenticate(request,username=username,password=password)
          if myuser:
               login(request,myuser)
               return HttpResponseRedirect(reverse("index"))
          else:
               return render(request,'home/login.html',{'message':"invalid credentials"})
     else:
          return render(request,'home/login.html')
     
def logout_view(request):
     logout(request)
     return render(request,'home/login.html',{'message':"Logged out"})
     