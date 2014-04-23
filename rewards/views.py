#encoding:utf-8

from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render
from rewards.models import Reward,Uncover,Reward_mes
from courses.models import Types,Tiny_type,Course,Lession,Course_comment
from users.models import Info,Teacher,News,Review_of_news,Message,Follow_topic,Follow_user,Follow_group,Follow_course,Post_reward,Post_course,Purchase,Good_news,Good_review_of_news
from django.utils import timezone
import re,md5,os,time,random

def reward(request):
	types=Types.objects.all()
	rewardTable=Reward.objects.all().order_by('-time')

	rewards=[]
	for r in rewardTable:
		areward=[]
		info=Info.objects.get(user_id=r.from_id)
		areward.append(info.img)		#0
		areward.append(r.id)		#1
		areward.append(r.name)		#2
		areward.append(r.price)		#3
		intro=r.introduce[0:70]
		intro=intro+'...'
		areward.append(intro)		#4
		typesTable=Types.objects.get(id=r.types_id)
		areward.append(typesTable.name)		#5
		rewards.append(areward)

	paginator = Paginator(rewards, 15)
	page = request.GET.get('page')
	try:
	    rewards = paginator.page(page)
	except PageNotAnInteger:
	    rewards = paginator.page(1)
	except EmptyPage:
	    rewards = paginator.page(paginator.num_pages)
	result=[]

	return render(request,'rewards/rewards.html',{'rewards':rewards,'types':types})



def rewards(request):
	if 'order' in request.GET:
		order=int(request.GET['order'])
	else:
		order=0

	if 'typeid' in request.GET:
		typeid=int(request.GET['typeid'])
	else:
		typeid=0
	
	types=Types.objects.all()

	if typeid==0:
		if order==4:
			rewardTable=Reward.objects.all().order_by('price')
		elif order==3:
			rewardTable=Reward.objects.all().order_by('-price')
		elif order==2:
			rewardTable=Reward.objects.all().order_by('-message_con')
		else:
			rewardTable=Reward.objects.all().order_by('-time')
	else:
		if order==4:
			rewardTable=Reward.objects.filter(types_id=int(typeid)).order_by('price')
		elif order==3:
			rewardTable=Reward.objects.filter(types_id=int(typeid)).order_by('-price')
		elif order==2:
			rewardTable=Reward.objects.filter(types_id=int(typeid)).order_by('-message_con')
		else:
			rewardTable=Reward.objects.filter(types_id=int(typeid)).order_by('-time')


	rewards=[]
	for r in rewardTable:
		areward=[]
		info=Info.objects.get(user_id=r.from_id)
		areward.append(info.img)		#0
		areward.append(r.id)		#1
		areward.append(r.name)		#2
		areward.append(r.price)		#3
		intro=r.introduce[0:70]
		intro=intro+'...'
		areward.append(intro)		#4
		typesTable=Types.objects.get(id=r.types_id)
		areward.append(typesTable.name)		#5
		rewards.append(areward)

	paginator = Paginator(rewards, 15)
	page = request.GET.get('page')
	try:
	    rewards = paginator.page(page)
	except PageNotAnInteger:
	    rewards = paginator.page(1)
	except EmptyPage:
	    rewards = paginator.page(paginator.num_pages)
	result=[]

	return render(request,'rewards/rewards.html',{'rewards':rewards,'types':types,'order':order,'typeid':typeid})



def rewardcreate(request):
	info=Info.objects.get(user_id=request.session['id'])
	user_name=info.user_name
	user_img=info.img
	types=Types.objects.all()

	return render(request,'rewards/rewardCreate.html',{'types':types,'user_name':user_name,'user_img':user_img,'user_id':request.session['id']})

def addReward(request):
	course_name=request.POST['course_name']
	course_intro=request.POST['course_intro']
	price=request.POST['price']
	belongtype=request.POST['belongtype']
	reward=Reward(types_id=request.POST['belongtype'],from_id=request.session['id'],name=request.POST['course_name'],introduce=request.POST['course_intro'],price=request.POST['price'],course_id=0)
	reward.save()
	reward.deadline_str=str(reward.deadline)
	reward_list=reward.deadline_str.split('.')
	deadline_str=reward_list[0]
	timeArray=time.strptime(deadline_str,"%Y-%m-%d %H:%M:%S")
	timeStamp=int(time.mktime(timeArray))
	x = time.localtime(timeStamp+2592000)
	reward.deadline=time.strftime('%Y-%m-%d %H:%M:%S',x)
	reward.save()

	return HttpResponseRedirect('../success/?course_name='+course_name+'&reward_id='+str(reward.id))

def success(request):
	course_name=request.GET['course_name']
	reward_id=int(request.GET['reward_id'])
	return render(request,'rewards/success.html',{'course_name':course_name,'reward_id':reward_id})


def thereward(request,id):
	thereward=Reward.objects.get(id=id)
	info=Info.objects.get(user_id=thereward.from_id)
	areward=[]
	areward.append(thereward.name)		#0
	areward.append(thereward.introduce)		#1
	areward.append(thereward.time)		#2
	areward.append(thereward.deadline)		#3
	areward.append(thereward.price)		#4
	areward.append(info.user_name)		#5
	areward.append(info.img)			#6
	Rcount = Reward.objects.filter(from_id=info.user_id).count()
	areward.append(Rcount)				#7
	SUCRcount = Reward.objects.filter(from_id=info.user_id).filter(to__isnull=False).count()
	areward.append(SUCRcount)			#8
	typesTable=Types.objects.get(id=thereward.types_id)
	areward.append(typesTable.name)			#9
	areward.append(id)					#10

	re_rewardTable=Reward_mes.objects.filter(reward_id=id).order_by('-time')
	re_rewards=[]
	for r in re_rewardTable:
		a_re_reward=[]
		info=Info.objects.get(user_id=r.from_id)
		a_re_reward.append(info.img)			#0
		a_re_reward.append(info.user_name)		#1
		a_re_reward.append(r.content)			#2
		a_re_reward.append(r.time)				#3
		a_re_reward.append(r.from_id)				#4
		re_rewards.append(a_re_reward)


	yellow_stars=range(0,info.credit)
	hollow_stars=range(0,(5-info.credit))

	return render(request,'rewards/theReward.html',{'areward':areward,'re_rewards':re_rewards,'yellow_stars':yellow_stars,'hollow_stars':hollow_stars})


def addreview(request):
	content=request.GET['content']
	reward_id=request.GET['reward_id']
	from_id=request.session['id']
	re_reward=Reward_mes(reward_id=reward_id,from_id=from_id,content=content)
	re_reward.save()
	info=Info.objects.get(user_id=from_id)
	
	return HttpResponse(str(info.img)+','+str(info.user_name)+','+str(from_id))



def uncover(request):
	reward_id=request.GET['reward_id']

	uncoverTable=Uncover(reward_id=reward_id,to=request.session['id'],status=1)
	uncoverTable.save()

	rewardTable=Reward.objects.get(id=reward_id)
	rewardTable.uncover_con=int(rewardTable.uncover_con)+1
	rewardTable.save()
	
	
	return HttpResponse(1)


