#encoding:utf-8

from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render
from users.models import Info,Follow_group,Message
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
	active=Follow_group.objects.filter(follow_group_id=group.id).order_by('-good_con')[0:5]
	actman=[]
	for act in active:
		each=[]
		info=Info.objects.get(user_id=act.user_id)
		each.append(info.user_name)
		each.append(info.img)
		each.append(act.good_con)
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
	t=Topic.objects.filter(group_id=group.id)
	topic=[]
	for k in t:
		each=[]
		i=Info.objects.get(user_id=k.user_id)
		each.append(i.user_name)     #0
		each.append(k.name)          #1
		each.append(k.last_time)     #2
		each.append(k.review_con)    #3
		each.append(k.id)	     #4
		topic.append(each)
	return render(request,'groups/theGroup.html',{'group':group,'status':status,'actman':actman,'message':mess,'havent':havent,'topic':topic})

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
	return render(request,'groups/theTopic.html',{'topic':topic,'user':user,'group':group})

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

