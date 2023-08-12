from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class posts(models.Model):
  title=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user")
  content=models.TextField()
  timestamp=models.DateTimeField(blank=True)
  likes=models.PositiveIntegerField(default=0)
  
  def serialise(self):
    return{
      "id":self.id,
      #"title":self.title.title,
      "content":self.content,
      "likes":self.likes
    }
  
  
  
class Like(models.Model):
    post=models.ForeignKey(posts,on_delete=models.PROTECT,related_name="post")
    user=models.ForeignKey(User,on_delete=models.PROTECT,related_name="likedby")
    

  
  
 
