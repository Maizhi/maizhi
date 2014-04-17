from django.db import models
from courses.models import Types

class Reward(models.Model):
	types=models.ForeignKey(Types)
	from_id=models.IntegerField()
	to=models.IntegerField(blank=True,null=True)
	message_con=models.IntegerField(default=0)
	uncover_con=models.IntegerField(default=0)
	course_id=models.IntegerField()
	name=models.CharField(max_length=199)
	introduce=models.TextField()
	time=models.DateTimeField(auto_now_add=True)
	deadline=models.DateTimeField(auto_now_add=True)
	price=models.FloatField()
	
class Uncover(models.Model):
	reward=models.ForeignKey(Reward)
	to=models.IntegerField()
	time=models.DateTimeField(auto_now_add=True)
	status=models.IntegerField(default=1)

class Reward_mes(models.Model):
	reward=models.ForeignKey(Reward)
	from_id=models.IntegerField()
	content=models.TextField()
	time=models.DateTimeField(auto_now_add=True)
 

