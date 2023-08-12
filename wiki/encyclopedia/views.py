from django.urls import reverse
from random import choice
from django.http import HttpResponseRedirect
from django.shortcuts import render,HttpResponse,redirect
import markdown
from . import util
from django import forms
import random







class nameform(forms.Form):
     
     your_title=forms.CharField(label="Title",max_length=120,widget=forms.TextInput( attrs={'class':"form-control"}))
     content=forms.CharField(label="content",widget=forms.Textarea(attrs={'class':"form-control",'rows':10,'cols':50}))


def index(request):
     
        
        return render(request, "encyclopedia/index.html",{"entries": util.list_entries()})
    


def create(request):
    if request.method=="POST":
        form=nameform(request.POST)
        
        if form.is_valid():
            title=form.cleaned_data['your_title']
            content=form.cleaned_data['content']
            
            util.save_entry(title,content)
            print("hello")
            return render(request,'encyclopedia/index.html',{"entries": util.list_entries()})
        else:
            return render(request,'encyclopedia/Newpage.html',{'form':nameform})  
            
            
    
    else:  
        print("hello")
        return render(request,'encyclopedia/Newpage.html',{'form':nameform})
    
def display_view(request,entry):
    content=util.get_entry(entry)
    if content is not None:
        return render(request,'encyclopedia/display.html',{'content':content,'entry':entry})
    else:
        return render(request,'encyclopedia/index.html')
    
class editpageform(forms.Form):
    edit_content=forms.CharField(widget=forms.Textarea(attrs={'class':"form-control",'rows':10,'cols':50}))
def edit(request,entry):
     form=editpageform(initial={'edit_content':util.get_entry(entry)})
     if request.method=="POST":
        update=editpageform(request.POST)
        print("hello")
        if update.is_valid():
            newcontent=update.cleaned_data['edit_content']
            util.save_entry(entry,newcontent)
            return render(request, "encyclopedia/index.html",{"entries": util.list_entries()})
        else:
            return render(request,'encyclopedia/edit.html',{'form':form,'entry':entry})
            
     else:
        form=editpageform(initial={'edit_content':util.get_entry(entry)})
        return render(request,'encyclopedia/edit.html',{'form':form,'entry':entry})
     
def random(request):
    entries=util.list_entries()
    if entries:
        title = choice(entries)
        return HttpResponseRedirect(reverse('display', args=[title]))
        # <!-- return redirect("encyclopedia:display",entry=random_entry) -->
    else:
        return HttpResponse("No entries available.")
    

         
            
        

    

