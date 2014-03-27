#encoding:utf-8

from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render
from users.models import Info,Follow_group,Message,Follow_topic,Follow_user
from groups.models import Group,Topic,Review_of_topic,Good_review_of_topic,Group_file
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt 
import re,md5,os,time,json,simplejson

def groups(request):
	gro=Group.objects.all()
	follow=Follow_group.objects.filter(user_id=request.session['id'])
	fg=[]
	for f in follow:
		fg.append(int(f.follow_group_id))
	group=[]
	for i in gro:
		if i.user_id==request.session['id']:
			pass
		else:
			each=[]
			each.append(i.img)     #0  
			each.append(i.name)    #1
			if i.id in fg:
				join=True
				each.append('1')   #2
			else:
				join=None
				each.append('0')   #2
			each.append(i.id)      #3
			group.append(each)
	m=Message.objects.filter(to=request.session['id']).order_by('-time')[0:5]
	mess=[]
	for k in m:
		each=[]
		name=Info.objects.get(user_id=k.from_id).user_name
		content=k.content
		each.append(name)
		each.append(content)
		mess.append(each)
	havent=0
	for n in m:
		if n.status==1:
			havent+=1
	return render(request,'groups/groups.html',{'groups':group,'fg':fg,'message':mess,'havent':havent})

def join(request):
	my=Follow_group.objects.filter(user_id=request.session['id'])
	group=Group.objects.get(id=request.GET['id'])
	follow=[]
	for i in my:
		follow.append(int(i.follow_group_id))
	if int(request.GET['id']) in follow:
		Follow_group.objects.filter(user_id=request.session['id']).get(follow_group_id=request.GET['id']).delete()
		crew_con=int(group.crew_con)-int(1)
		group.crew_con=crew_con
		group.save()
	else:
		Follow_group(user_id=request.session['id'],follow_group_id=request.GET['id'],status='1',topic_con='0',good_con='0',review_con='0',file_con='0').save()
		crew_con=int(group.crew_con)+int(1)
		group.crew_con=crew_con
		group.save()
	return HttpResponse('OK !')

def thegroup(request,id):
	group=Group.objects.get(id=id)
	if 'groupImg' in request.FILES:
		image=request.FILES['groupImg']
		pattern=re.compile(r'\.') 
		head=pattern.split(str(image))
		head[0]=group.name
		filename=head[0]+'.'+head[1]
		dirs ='templates/picture/group/image/'+filename
		content = image.read()
		if os.path.isfile(dirs):
			os.remove(dirs) 
		fp=open(dirs, 'wb')
		fp.write(content)
		fp.flush()
		fp.close()
		group.img=filename
		group.save()
	f=Follow_user.objects.filter(user_id=request.session['id'])
	follow=[]
	for  m in f:
		follow.append(m.follow_user_id)
	active=Follow_group.objects.filter(follow_group_id=group.id).order_by('-good_con')[0:5]
	actman=[]
	for act in active:
		if act.user_id in follow:
			pass
		elif act.user_id == request.session['id']:
			pass
		else:
			each=[]
			info=Info.objects.get(user_id=act.user_id)
			each.append(info.user_name)    #0
			each.append(info.img)          #1
			each.append(act.good_con)	   #2
			each.append(act.user_id)	   #3
			actman.append(each)
	if request.session['id']==group.user_id:
		status='1'
	else:
		f=Follow_group.objects.filter(user_id=request.session['id'])
		follow=[]
		for i in f:
			follow.append(i.follow_group_id)
		if group.id in follow:
			status='2'
		else:
			status='3'
	m=Message.objects.filter(to=request.session['id']).order_by('-time')[0:5]
	mess=[]
	for k in m:
		each=[]
		name=Info.objects.get(user_id=k.from_id).user_name
		content=k.content
		each.append(name)
		each.append(content)
		mess.append(each)
	havent=0
	for n in m:
		if n.status==1:
			havent+=1
	limit = 15
	topics=Topic.objects.filter(group_id=group.id).order_by('-time')
	paginator = Paginator(topics, limit)
	page = request.GET.get('page')
	try:
	    topics = paginator.page(page)
	except PageNotAnInteger:
	    topics = paginator.page(1)
	except EmptyPage:
	    topics = paginator.page(paginator.num_pages)
	topic=[]
	for k in topics:
		each=[]
		i=Info.objects.get(user_id=k.user_id)
		each.append(i.user_name)     #0
		each.append(k.name)          #1
		each.append(k.last_time)     #2
		each.append(k.review_con)    #3
		each.append(k.id)            #4
		topic.append(each)
	return render(request,'groups/theGroup.html',{'group':group,'status':status,'actman':actman,'message':mess,'havent':havent,'topic':topic,'topics':topics})

def topiccreate(request,id):
	group=Group.objects.get(id=id)
	m=Message.objects.filter(to=request.session['id']).order_by('-time')[0:5]
	mess=[]
	for k in m:
		each=[]
		name=Info.objects.get(user_id=k.from_id).user_name
		content=k.content
		each.append(name)
		each.append(content)
		mess.append(each)
	havent=0
	for n in m:
		if n.status==1:
			havent+=1
	return render(request,'groups/topicCreate.html',{'group':group,'message':mess,'havent':havent})

@csrf_exempt
def publish(request):
	try:
		content=request.POST['editor'].replace('*','+')
		content=content.replace('}',';')
		topic=Topic(group_id=request.POST['group'],user_id=request.session['id'],name=request.POST['title'],content=content)
		topic.save()
		return HttpResponse(topic.id)
	except:
		return HttpResponse('Wrong')

def thetopic(request,id):
	topic=Topic.objects.get(id=id)
	user=Info.objects.get(user_id=topic.user_id)
	group=Group.objects.get(id=topic.group_id)
	m=Message.objects.filter(to=request.session['id']).order_by('-time')[0:5]
	mess=[]
	for k in m:
		each=[]
		name=Info.objects.get(user_id=k.from_id).user_name
		content=k.content
		each.append(name)
		each.append(content)
		mess.append(each)
	havent=0
	for n in m:
		if n.status==1:
			havent+=1
	competence=None
	if group.user_id==request.session['id']:
		competence=True
	recommend=Topic.objects.filter(group_id=group.id).order_by('-review_con')[0:5]
	c=Follow_topic.objects.filter(user_id=request.session['id'])
	collect=[]
	for j in c:
		collect.append(j.follow_topic_id)
	abord=None
	if topic.id in collect:
		abord=True
	limit = 15
	topics=Review_of_topic.objects.filter(topic_id=topic.id).order_by('-time')
	paginator = Paginator(topics, limit)
	page = request.GET.get('page')
	try:
	    topics = paginator.page(page)
	except PageNotAnInteger:
	    topics = paginator.page(1)
	except EmptyPage:
	    topics = paginator.page(paginator.num_pages)
	review=[]
	for r in topics:
		each=[]
		each.append(r.content)                        #0
		each.append(r.time)                           #1
		each.append(r.good_con)                       #2
		each.append(r.review_con)                     #3
		info=Info.objects.get(user_id=r.from_id)
		each.append(info.user_name)                   #4
		each.append(info.img)                         #5
		review.append(each)
	return render(request,'groups/theTopic.html',{'topic':topic,'user':user,'group':group,'message':mess,'havent':havent,'competence':competence,'recommend':recommend,'abord':abord,'review':review,'topics':topics})

def collect(request):
	my=Follow_topic.objects.filter(user_id=request.session['id'])
	topic=Topic.objects.get(id=request.GET['id'])
	follow=[]
	for i in my:
		follow.append(int(i.follow_topic_id))
	if int(request.GET['id']) in follow:
		Follow_topic.objects.filter(user_id=request.session['id']).get(follow_topic_id=request.GET['id']).delete()
		collect_con=int(topic.collect_con)-int(1)
		topic.collect_con=collect_con
		topic.save()
	else:
		Follow_topic(user_id=request.session['id'],follow_topic_id=request.GET['id']).save()
		collect_con=int(topic.collect_con)+int(1)
		topic.collect_con=collect_con
		topic.save()
	return HttpResponse('1')

def comment(request):
	result=Review_of_topic(topic_id=request.GET['id'],from_id=request.session['id'],content=request.GET['content'])
	result.save()
	topic=Topic.objects.get(id=request.GET['id'])
	review_con=int(topic.review_con)+int(1)
	topic.review_con=review_con
	topic.save()
	return HttpResponse(result.id)

def change(request):
	group=Group.objects.get(id=request.GET['id'])
	group.introduce=request.GET['intro']
	group.save()
	return HttpResponse('1')

def groupcreate(request):
	try:
		if Group.objects.filter(name=request.POST['groupName']):
			return HttpResponse('小组已存在 ! ')
		else:
			if 'groupImg' in request.FILES:
				image=request.FILES['groupImg']
				pattern=re.compile(r'\.') 
				head=pattern.split(str(image))
				#tj=str(timezone.now())
				#tj=tj.split('.')
				#timej=time.mktime(time.strptime(tj[0],'%Y-%m-%d %H:%M:%S'))
				head[0]=request.POST['groupName']
				filename=head[0]+'.'+head[1]
				dirs ='templates/picture/group/image/'+filename
				content = image.read()
				if os.path.isfile(dirs):
					os.remove(dirs) 
				fp=open(dirs, 'wb')
				fp.write(content)
				fp.flush()
				fp.close()
			else:
				filename=None
			g=Group(name=request.POST['groupName'],introduce=request.POST['groupIntro'],img=filename,user_id=request.session['id'])
			g.save()
			return render(request,'groups/success.html',{'g':g.id})
	except:
		m=Message.objects.filter(to=request.session['id']).order_by('-time')[0:5]
		mess=[]
		for k in m:
			each=[]
			name=Info.objects.get(user_id=k.from_id).user_name
			content=k.content
			each.append(name)
			each.append(content)
			mess.append(each)
		havent=0
		for n in m:
			if n.status==1:
				havent+=1
		info=Info.objects.get(user_id=request.session['id'])
		return render(request,'groups/groupCreate.html',{'info':info,'message':mess,'havent':havent})

