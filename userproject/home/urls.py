from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.index,name="home"),
    path('login', views.loginuser,name="loginuser"),
    path('logout', views.logoutuser,name="logoutuser"),
    #path('register', views.register,name="register"),
    
]