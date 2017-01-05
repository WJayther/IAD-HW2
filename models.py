from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.

class MyUser(AbstractUser):
	follows = models.ManyToManyField('self',related_name='followers',symmetrical=False)
	#,limit_choices_to={'to_myuser':not id} not working
	# Fix it with forms (them are not admins anyway)

class Bullet(models.Model):
	name = models.CharField(max_length=30, verbose_name='Заголовок')
	description = models.CharField(max_length=255, verbose_name='Объявление')
	datetime = models.DateTimeField(auto_now=True, verbose_name='Время публикации')
	user_posted = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор', related_name='bullets')
