from django.db import models

class Register(models.Model):
	email=models.EmailField()
	password=models.CharField(max_length=128)
	status=models.IntegerField(default=1)
	time=models.DateTimeField(auto_now_add=True)
