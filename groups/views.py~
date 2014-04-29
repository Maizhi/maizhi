#encoding:utf-8

from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render
from users.models import Info,Follow_group,Message,Follow_topic,Follow_user
from groups.models import Group,Topic,Review_of_topic,Good_review_of_topic,Group_file
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re,md5,os,time,json,qiniu.io,qiniu.conf,qiniu.rs,base64

class PutPolicy(object):
    scope = 'maizhi'         
    expires = 3600       
    callbackUrl = None
    callbackBody = None
    returnUrl = None
    returnBody = None
    endUser = None
    asyncOps = None

    def __init__(self, scope):
        self.scope = scope

qiniu.conf.ACCESS_KEY = "EW8idy4EFnJDBicDJZhPIVIVDU9AL0g4waW5MNtJ"
qiniu.conf.SECRET_KEY = "C1qaP_-sgjVgQb6GGHJ-vCle0qTiGI8qtbgOumOB"

def groups(request):
	info=Info.objects.get(user_id=request.session['id'])
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
			each.append(i.domain)  #4
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
	return render(request,'groups/groups.html',{'groups':group,'fg':fg,'message':mess,'havent':havent,'info':info})

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
			user=Follow_group.objects.filter(follow_group_id=group.id).get(user_id=request.session['id'])
			if int(user.status)==int(1):
				status='2'
			else:
				status='4'
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
	recommend=Topic.objects.filter(group_id=group.id).order_by('-review_con')[0:5]
	limit = 15
	topics=Topic.objects.filter(group_id=group.id).order_by('-last_time')
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
		each.append(k.user_id)       #5
		try:
			user=Follow_group.objects.filter(follow_group_id=group.id).get(user_id=k.user_id)
			each.append(user.status) #6
		except:
			each.append('3')         #6
		if k.user_id == group.user_id:
			each.append('1')         #7
		else:
			each.append('2')         #7
		topic.append(each)
	info=Info.objects.get(user_id=request.session['id'])
	return render(request,'groups/theGroup.html',{'info':info,'group':group,'status':status,'actman':actman,'message':mess,'havent':havent,'topic':topic,'topics':topics,'recommend':recommend})

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
	info=Info.objects.get(user_id=request.session['id'])
	return render(request,'groups/topicCreate.html',{'info':info,'group':group,'message':mess,'havent':havent})

@csrf_exempt
def publish(request):
	#try:
		policy = qiniu.rs.PutPolicy('mztopic')
		uptoken = policy.token()
		content=request.POST['editor'].replace('*','+')
		content=content.replace('}',';')
		image=re.findall("src=\"(.+?)\"",content)
		img=[]
		for i in image:
			st=time.time()
			dirs ='templates/picture/topic/'+str(st)
			if os.path.isfile(dirs):
				os.remove(dirs) 
			frd=str(i).split(',')
			decode=base64.decodestring(frd[1])
			f=open(dirs,'w')
			f.write(decode)
			f.close()
			ret=qiniu.io.put_file(uptoken,str(st),r"/home/tron/Maizhi/templates/picture/topic/"+str(st))
			if ret:
				os.remove(dirs)
			domain="http://mztopic.qiniudn.com/"
			img.append(domain+str(st))
		for j in img:
			start=content.find("src=\"data")
			start=int(start)+int(5)
			end=content.find("\"",start)
			end=int(end)
			content=content.replace(content[start:end],j)
		#tname=time.time()
		#dirs ='templates/topic/'+str(tname)
		#if os.path.isfile(dirs):
		#	os.remove(dirs) 
		#fp=open(dirs, 'wb')
		#fp.write(content)
		#fp.flush()
		#fp.close()
		topic=Topic(group_id=request.POST['group'],user_id=request.session['id'],name=request.POST['title'],content=content)
		topic.save()
		#return HttpResponse(content)
		return HttpResponse(int(topic.id))
	#except:
	#	return HttpResponse('Wrong')	

def thetopic(request,id):
	#try:
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
			each.append(r.content)         	  	  #0
			each.append(r.time)                              	 #1
			each.append(r.good_con)                        #2
			each.append(r.review_con)                     #3
			info=Info.objects.get(user_id=r.from_id)
			each.append(info.user_name)                   #4
			each.append(info.img)                         #5
			each.append(r.id)                             #6
			review.append(each)
		info=Info.objects.get(user_id=request.session['id'])
		return render(request,'groups/theTopic.html',{'info':info,'topic':topic,'user':user,'group':group,'message':mess,'havent':havent,'competence':competence,'recommend':recommend,'abord':abord,'review':review,'topics':topics})
	#except:
	#	return HttpResponse('404')

def good(request):
	entire=Good_review_of_topic.objects.filter(review_of_topic_id=request.GET['id'])
	for i in entire:
		if request.session['id']==i.user_id:
			return HttpResponse('2')
	Good_review_of_topic(review_of_topic_id=request.GET['id'],user_id=request.session['id']).save()
	review=Review_of_topic.objects.get(id=request.GET['id'])
	topic=Topic.objects.get(id=review.topic_id)
	n=Follow_group.objects.filter(user_id=request.session['id']).get(follow_group_id=topic.group_id)
	g=int(n.good_con)+int(1)
	n.good_con=g
	n.save()
	r=int(review.good_con)+1
	review.good_con=r
	review.save()
	return HttpResponse('1')

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
			policy = qiniu.rs.PutPolicy('mzgroup')
			uptoken = policy.token()
			if 'groupImg' in request.FILES:
				tj=time.time()
				image=request.FILES['groupImg']
				dirs ='templates/picture/group/image/'+str(tj)
				content = image.read()
				if os.path.isfile(dirs):
					os.remove(dirs) 
				fp=open(dirs, 'wb')
				fp.write(content)
				fp.flush()
				fp.close()
				domain="http://mzgroup.qiniudn.com"
				ret=qiniu.io.put_file(uptoken,str(tj),r"/home/tron/Maizhi/templates/picture/group/image/"+str(tj))
				if ret:
					os.remove(dirs)
			else:
				filename=None
			g=Group(name=request.POST['groupName'],introduce=request.POST['groupIntro'],img=str(tj),domain=domain,user_id=request.session['id'])
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

def download(request,group):
	group=Group.objects.get(id=group)
	space=float(group.filespace)/float(2097152)*100
	free=float(group.filespace)/1024
	competence=None
	if request.session['id']==group.user_id:
		competence=True
	limit = 15
	files=Group_file.objects.filter(group_id=group.id).order_by('-time')
	paginator = Paginator(files, limit)
	page = request.GET.get('page')
	try:
	    files = paginator.page(page)
	except PageNotAnInteger:
	    files = paginator.page(1)
	except EmptyPage:
	    files = paginator.page(paginator.num_pages)
	document=[]
	for f in files:
		each=[]
		info=Info.objects.get(user_id=f.user_id)
		each.append(info.user_name)     #0
		each.append(f.user_id)			#1
		each.append(f.down_con)			#2
		each.append(f.name)				#3
		each.append(f.introduce)		#4
		each.append(f.time)				#5
		each.append(f.file_path)		#6
		each.append(f.id)				#7
		document.append(each)
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
	return render(request,'groups/download.html',{'group':group,'space':space,'competence':competence,'message':mess,'havent':havent,'document':document,'files':files,'free':free})

def upload(request,group):
	group=Group.objects.get(id=group)
	space=float(group.filespace)/float(2097152)*100
	free=float(group.filespace)/1024
	try:
		user=request.session['id']
		intro=request.POST['intro']
		if 'files' in request.FILES:
			filesize=request.FILES['files'].size
			filename=request.FILES['files'].name
			pattern=re.compile(r'\.') 
			format=pattern.split(str(filename))
			realname=str(time.time())+"."+format[1]
			dirs ='templates/picture/group/file/'+realname
			content = request.FILES['files'].read()
			if os.path.isfile(dirs):
				os.remove(dirs) 
			fp=open(dirs, 'wb')
			fp.write(content)
			fp.flush()
			fp.close()
		else:
			f=None
		result=Group_file(user_id=user,group_id=group.id,introduce=intro,name=filename,file_path=realname,file_length=int(filesize)/int(1024))
		result.save()
		group.filespace=int(group.filespace)-int(filesize)/int(1024)
		if group.filespace<=0:
			leftspace='0'
		else:
			leftspace='1'
			group.save()
		return render(request,'groups/upload.html',{'result':'1','space':space,'group':group,'space':space,'filesize':filesize,'free':free})
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
		return render(request,'groups/upload.html',{'message':mess,'havent':havent,'group':group,'space':space,'free':free})

def down(request):
	files=Group_file.objects.get(id=request.GET['id'])
	down=int(files.down_con)+int(1)
	files.down_con=down
	files.save()
	return HttpResponse('ok')

def delete(request):
	files=Group_file.objects.get(id=request.GET['id'])
	group=Group.objects.get(id=files.group_id)
	group.filespace=int(group.filespace)+int(files.file_length)
	group.save()
	files.delete()
	return HttpResponse('OK')

def deleteTopic(request):
	topic=Topic.objects.get(id=request.GET['id'])
	topic.delete()
	return HttpResponse('OK')

def deleteReview(request):
	review=Review_of_topic.objects.get(id=request.GET['id'])
	review.delete()
	return HttpResponse('OK')

def ban(request):
	user=Follow_group.objects.get(user_id=request.GET['id'])
	if user.status==2:
		user.status=1
		user.save()
		return HttpResponse('2')
	else:
		user.status=2
		user.save()
		return HttpResponse('1')

def cccomment(request):	
	re_id=int(request.GET['id'])
	reoftopic=Review_of_topic.objects.get(id=re_id)
	rre_topicid=reoftopic.topic_id
	rre_fromid=request.session['id']
	rre_to=reoftopic.from_id
	rre=Review_of_topic(topic_id=rre_topicid,from_id=rre_fromid,to=rre_to,content=request.GET['content'],to_review=re_id)
	rre.save()
	rre_id=rre.id
	reviewCon=int(reoftopic.review_con)+int(1)
	reoftopic.review_con=reviewCon
	reoftopic.save()
	topic=Topic.objects.get(id=rre_topicid)
	review_con=int(topic.review_con)+int(1)
	topic.review_con=review_con
	topic.save()
	info=Info.objects.get(user_id=request.session['id'])
	name=info.user_name
	img=info.img
	

	return HttpResponse(str(rre_id)+','+str(img)+','+str(name)+','+str(0)+','+str(0))
	#return HttpResponse(re_id)	
	
