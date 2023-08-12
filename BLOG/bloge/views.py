from django.shortcuts import render,HttpResponse,redirect
from bloge.models import post,Blogcomment
from django.contrib import messages


# Create your views here.
def bloghome(request):
    allpost=post.objects.all()
    context={
        'allposts':allpost
    }
    return render(request,'blog/bloghome.html',context)


def blogpost(request,slug):
    posts=post.objects.filter(slug=slug).first()
    comments=Blogcomment.objects.filter(posts=posts)
    context={
        'post':posts,
        'comments':comments,
        'user':request.user
        
    }
    

    return render(request,'blog/blogpost.html',context)


def postcomment(request):
    if request.method=='POST':
        
        comment=request.POST.get("comment")
        user=request.user
        postsSno=request.POST.get("postSno")
        posts=post.objects.get(sno=postsSno)
        
        comment=Blogcomment(comment=comment,user=user,posts=posts)
        comment.save()
        messages.success(request,"your comment has been posted successfully ")
        print("hello")
        
    
    return redirect(f"/blog/{posts.slug}")
