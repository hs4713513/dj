from django.contrib import admin
from django.urls import path,include
from bloge import views

urlpatterns = [
   #path('admin/', admin.site.urls),
   path('postcomment',views.postcomment,name='postcomment'),
    path('',views.bloghome,name='bloghome'),
    
    path('<str:slug>',views.blogpost,name='blogpost')
    
    # api for posting comment...
    
]
