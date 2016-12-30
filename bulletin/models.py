from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Bullet(models.Model):
	name = models.CharField(max_length=30)
	description = models.CharField(max_length=255)
	datetime = models.DateTimeField(auto_now=True)
	user_posted = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bullets')

class MyUser(AbstractUser):
	regdate = models.DateTimeField(auto_now_add=True)
	
	class Meta(AbstractUser.Meta):
		swappable = 'AUTH_USER_MODEL'
