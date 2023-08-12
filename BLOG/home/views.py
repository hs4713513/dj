from django.shortcuts import render,HttpResponse,redirect
from home.models import Contact
from bloge.models import post
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate



# html pages
def home(request):
     allpost=post.objects.all()
     context={
        'allposts':allpost
     }
    
     return render(request,'home/home.html',context)
def about(request):
    return render(request,'home/about.html')
def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']
        #global context
        #  context={
        #     'name':name,'email':email,'phone':phone,'content':content
        # }
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request,"please fill the form correctly !")
            return render(request,'home/contact.html')
        else:
            contact=Contact(name=name,email=email,phone=phone,content=content)
            contact.save()
            messages.success(request,"Message has been sent successfully...")
        
        
        
    return render(request,'home/contact.html')
def search(request):
    #allposts=post.objects.all()
    query=request.GET['query']
    if len(query)>78:
        allposts=post.objects.none()
    else:
        allpoststitle=post.objects.filter(title__icontains=query)
        allpostcontent=post.objects.filter(content__icontains=query)
        allposts=allpoststitle.union(allpostcontent)
    if allposts.count()==0:
        messages.error(request,"please refine your query !")
    params={'allposts':allposts,'query':query}
    return render(request,'home/search.html',params)

# authentication API's

def handlesignup(request):
    if request.method=='POST':
        #get the post parameters...
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        
        
        #check for erronious credentials
        if len(username)>10:
            messages.error(request,"username should less than 10 char")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request,"Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request,"Enter the same password as before, for verification")
            return redirect('home')
        
        
             
         
        #create user
        myuser=User.objects.create_user(username,email,pass2)
        myuser.first_name=fname
        myuser.last_name=lname
        #myuser.email=email
        myuser.save()
        messages.success(request,"user has been registered successfully")
        return redirect('home')
        
        
        
    else:
         return HttpResponse('404 - Not Found')
     
def handlelogin(request):
    if request.method=='POST':
        #get the post parameters...
        loginusername=request.POST['loginusername']
        loginpass=request.POST['pass']
        user=authenticate(username=loginusername,password=loginpass)
        
        if user is not None:
            login(request,user)
            messages.success(request,"successfully logged In")
            return redirect('home')
        
        else:
             messages.error(request,"invalid credentials,please try again")
             return redirect('home')
    else:
        return HttpResponse('404 - not found')
               
        
        
        
    return HttpResponse('login')
    
    
def handlelogout(request):
    logout(request)
    messages.success(request,"successfully logged out")
    return redirect('home')

      
     
    
    
    
    
    
    
    
    


