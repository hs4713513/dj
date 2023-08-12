from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("newpage", views.create, name="newpage"),
    path("display/<entry>", views.display_view, name="display"),
    path("edit/<entry>", views.edit, name="edit"),
    path("random", views.random, name="random"),
    
    
]
