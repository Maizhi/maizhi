from django.db import models
from login.models import Register

class Info(models.Model):
	user=models.ForeignKey(Register)
	user_name=models.CharField(max_length=49)
	work=models.CharField(max_length=99,blank=True,null=True)
	position=models.CharField(max_length=19,blank=True,null=True)
	sign=models.CharField(max_length=49,blank=True,null=True)
	introduce=models.TextField(blank=True,null=True)
	birthday=models.CharField(max_length=19,blank=True,null=True)
	sex=models.IntegerField(blank=True,null=True)
	img=models.ImageField(upload_to='templates/picture/avatar/',blank=True,null=True)
	follow_group_con=models.IntegerField(default=0)
	fan_con=models.IntegerField(default=0)
	focus_con=models.IntegerField(default=0)
	constellation=models.CharField(max_length=12,blank=True,null=True)
	tag=models.CommaSeparatedIntegerField(max_length=255,blank=True,null=True)
	credit=models.IntegerField(default=0)

class Teacher(models.Model):
	user=models.ForeignKey(Register)
	real_name=models.CharField(max_length=19)
	alipay=models.CharField(max_length=49)
	identity=models.CharField(max_length=20)
	tel=models.CharField(max_length=19)
	identity_img=models.ImageField(upload_to='templates/picture/ID/',blank=True,null=True)

class News(models.Model):
	user=models.ForeignKey(Register)
	content=models.TextField()
	good_con=models.IntegerField()
	share_con=models.IntegerField()
	review_con=models.IntegerField()
	img=models.ImageField(upload_to='templates/picture/news/',blank=True,null=True)
	time=models.DateTimeField(auto_now_add=True)

class Review_of_news(models.Model):
	news=models.ForeignKey(News)
	content=models.TextField()
	from_id=models.IntegerField()
	to=models.IntegerField()
	good_con=models.IntegerField()
	time=models.DateTimeField(auto_now_add=True)

class Message(models.Model):
	status=models.IntegerField()
	from_id=models.IntegerField()
	to=models.IntegerField()
	content=models.TextField()
	time=models.DateTimeField(auto_now_add=True)

class Follow_user(models.Model):
	user=models.ForeignKey(Register)
	follow_user_id=models.IntegerField()

class Follow_topic(models.Model):
	user=models.ForeignKey(Register)
	follow_topic_id=models.IntegerField()

class Follow_group(models.Model):
	user=models.ForeignKey(Register)
	follow_group_id=models.IntegerField()
	topic_con=models.IntegerField()
	good_con=models.IntegerField()
	review_con=models.IntegerField()
	file_con=models.IntegerField()
	status=models.IntegerField()

class Follow_course(models.Model):
	user=models.ForeignKey(Register)
	follow_course_id=models.IntegerField()

class Post_reward(models.Model):
	user=models.ForeignKey(Register)
	uncover=models.IntegerField()
	post_reward_id=models.IntegerField()
	status=models.IntegerField()

class Post_course(models.Model):
	user=models.ForeignKey(Register)
	post_course_id=models.IntegerField()
	status=models.IntegerField()

class Purchase(models.Model):
	user=models.ForeignKey(Register)
	purchase_id=models.IntegerField()
	teacher_id=models.IntegerField()
	process=models.CharField(max_length=255)
	time=models.DateTimeField(auto_now_add=True)

class Good_news(models.Model):
	news=models.ForeignKey(News)
	user_id=models.IntegerField()

class Good_review_of_news(models.Model):
	review_of_news=models.ForeignKey(Review_of_news)
	user_id=models.IntegerField()