from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("display/<int:list_id>/", views.display, name="display"),
    path("add/<int:list_id>/", views.add, name="add"),
    path("newbid/<int:list_id>/", views.newbid, name="newbid"),
    path("create", views.create, name="create"),
    path("displaywatch", views.displaywatch, name="displaywatch"),
    path("addcomments/<int:list_id>/", views.addcomments, name="addcomments"),
    path("closea/<int:list_id>/", views.closea, name="closea"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
