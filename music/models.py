from django.db import models
from django.contrib.auth.models import Permission, User

from django.urls import reverse

# Create your models here.
class Album(models.Model):
    user = models.ForeignKey(User, default=1 , on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    artist = models.CharField(max_length=50)
    album_file = models.FileField(null=True)
    is_public = models.BooleanField(default='False')
    def get_absolute_url(self):
        return reverse("music:detail", kwargs={"id": self.pk})
    def __str__(self):
        return self.title+' - '+self.artist

class Song(models.Model):
   album = models.ForeignKey(Album, on_delete=models.CASCADE)
   title = models.CharField(max_length=50) 
   song_file = models.FileField(null=True)
   is_favorite = models.BooleanField(default='False')
   is_public = models.BooleanField(default='False')
   def __str__(self):
        return self.title 
