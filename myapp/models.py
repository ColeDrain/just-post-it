from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=100)
	body = models.TextField()
	author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, related_name='posts')

	def __str__(self):
		return self.title