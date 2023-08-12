from django.shortcuts import render,HttpResponse
from datetime import datetime
from Home.models import Contact
from django.contrib import messages
from django import forms



    
# Create your views here.
def index(request):
    cont={
        'variable':"this is  sent"
    }
    
    
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def services(request):
    return render(request,'services.html')
def contact(request):
    if request.method=="POST":
        
        
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        desc=request.POST.get('desc')
        obj=Contact(name=name,email=email,phone=phone,desc=desc,date=datetime.today())
        obj.save()
        messages.success(request,"Your Message Has Been Sent!")
    return render(request,'contact.html')


    
