from django.contrib import admin
from bloge.models import post,Blogcomment

# Register your models here.
admin.site.register((post,Blogcomment))
#created a tuple to register multiple models..
#admin.site.register(Blogcomment)
