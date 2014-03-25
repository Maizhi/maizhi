#encoding:utf-8

from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render
from users.models import Info,Follow_group,Message
from groups.models import Group,Topic,Review_of_topic,Good_review_of_topic,Group_file
from django.utils import timezone
import re,md5,os,time

def groups(request):
	gro=Group.objects.all()[0:10]
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
	follow=[]
	for i in my:
		follow.append(int(i.follow_group_id))
	if int(request.GET['id']) in follow:
		Follow_group.objects.filter(user_id=request.session['id']).get(follow_group_id=request.GET['id']).delete()
	else:
		Follow_group(user_id=request.session['id'],follow_group_id=request.GET['id'],status='1',topic_con='0',good_con='0',review_con='0',file_con='0').save()
	return HttpResponse('OK !')

def thegroup(request,id):
	return render(request,'groups/theGroup.html')

def topiccreate(request,id):
	return render(request,'groups/topicCreate.html')

def thetopic(request,id):
	return render(request,'groups/theTopic.html')

def groupcreate(request):
	try:
		if Group.objects.filter(name=request.POST['groupName']):
			return HttpResponse('小组已存在 ! ')
		else:
			if 'groupImg' in request.FILES:
				image=request.FILES['groupImg']
				pattern=re.compile(r'\.') 
				head=pattern.split(str(image))
				tj=str(timezone.now())
				tj=tj.split('.')
				timej=time.mktime(time.strptime(tj[0],'%Y-%m-%d %H:%M:%S'))
				head[0]=str(timej)
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

