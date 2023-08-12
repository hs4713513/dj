from django.db import models

# Create your models here.
class data(models.Model):
    title=models.CharField(max_length=120)
    content=models.TextField()
