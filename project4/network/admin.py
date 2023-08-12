from django.contrib import admin
from .models import User,posts,Like
# Register your models here.
admin.site.register(User)
admin.site.register(posts)
admin.site.register(Like)
