from django.db import models

class Group(models.Model):
	tag=models.CommaSeparatedIntegerField(max_length=99)
	topic_con=models.IntegerField(default=0)
	filespace=models.IntegerField(default=2097152)
	user_id=models.IntegerField()
	introduce=models.TextField()
	img=models.ImageField(upload_to='templates/picture/group/image/',blank=True,null=True)
	name=models.CharField(max_length=99)
	crew_con=models.IntegerField(default=1)
	status=models.IntegerField(default=1)
	time=models.DateTimeField(auto_now_add=True)


class Topic(models.Model):
	group=models.ForeignKey(Group)
	user_id=models.IntegerField()
	share_con=models.IntegerField(default=0)
	collect_con=models.IntegerField(default=0)
	review_con=models.IntegerField(default=0)
	name=models.CharField(max_length=99)
	content=models.TextField()
	img=models.ImageField(upload_to='templates/picture/topic/',blank=True,null=True)
	time=models.DateTimeField(auto_now_add=True)
	last_time=models.DateTimeField(auto_now=True)

class Review_of_topic(models.Model):
	topic=models.ForeignKey(Topic)
	from_id=models.IntegerField()
	to=models.IntegerField(blank=True,null=True)
	content=models.TextField()
	good_con=models.IntegerField(default=0)
	review_con=models.IntegerField(default=0)
	to_review=models.IntegerField(blank=True,null=True)
	time=models.DateTimeField(auto_now_add=True)

class Good_review_of_topic(models.Model):
	review_of_topic=models.ForeignKey(Review_of_topic)
	user_id=models.IntegerField()

class Group_file(models.Model):
	group=models.ForeignKey(Group)
	user_id=models.IntegerField()
	name=models.CharField(max_length=99)
	introduce=models.TextField()
	file_path=models.FileField(upload_to='templates/picture/group/file/')
	down_con=models.IntegerField(default=0)
	file_length=models.CharField(max_length=50)
	time=models.DateTimeField(auto_now_add=True)

