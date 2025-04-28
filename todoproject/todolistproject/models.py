from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(upload_to='profile_pics', default='default.jpg')

    def __str__(self):
     return self.user.username

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    due = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
      return self.task
# Create your models here.
