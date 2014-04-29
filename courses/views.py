#encoding:utf-8

from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render
from courses.models import Types,Tiny_type,Course,Lession,Course_comment
from login.models import Register
from users.models import Info,Teacher,News,Review_of_news,Message,Follow_topic,Follow_user,Follow_group,Follow_course,Post_reward,Post_course,Purchase,Good_news,Good_review_of_news
from django.utils import timezone 
from PIL import Image
from django.contrib import messages
import re,md5,os,time,qiniu.io,qiniu.conf,qiniu.rs

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

def types(request):
	info=Info.objects.get(user_id=request.session['id'])
	types=Types.objects.all()
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
	course=Course.objects.all().order_by('-grade')[0:20]
	c=Follow_course.objects.filter(user_id=request.session['id'])
	follow=[]
	courses=[]
	for j in c:
		follow.append(j.follow_course_id)
	for i in course:
		if i.id in follow:
			pass
		else:
			each=[]
			each.append(i.domain)		#0
			each.append(i.img)		#1
			each.append(i.id)		#2
			each.append(i.name)		#3
			courses.append(each)
	return render(request,'courses/types.html',{'info':info,'message':mess,'havent':havent,'types':types,'courses1':courses[0:4],'courses1':courses[0:4],'courses2':courses[5:8],'courses3':courses[9:13]})

def tinytypes(request,ty):
	tiny=Tiny_type.objects.filter(types_id=int(ty))
	types=Types.objects.get(id=int(ty))
	info=Info.objects.get(user_id=request.session['id'])
	return render(request,'courses/tinyTypes.html',{'info':info,'tiny':tiny,'types':types})

def courselist(request,id):
	info=Info.objects.get(user_id=request.session['id'])
	course=Course.objects.filter(tiny_type_id=id).order_by('grade')
	tiny=Tiny_type.objects.get(id=id)
	types=Types.objects.get(id=tiny.types_id)
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
	limit = 10
	paginator = Paginator(course, limit)
	page = request.GET.get('page')
	try:
	    course = paginator.page(page)
	except PageNotAnInteger:
	    course = paginator.page(1)
	except EmptyPage:
	    course = paginator.page(paginator.num_pages)
	result=[]
	for i in course:
		each=[]
		each.append(i.img)			#0
		each.append(i.name)			#1
		each.append(i.introduce)	#2
		each.append(i.price)		#3
		k=Info.objects.get(user_id=i.teacher_id)
		each.append(k.user_name)	#4
		each.append(i.id) 			#5
		each.append(i.grade) 		#6
		each.append(i.grade_con)	#7
		each.append(i.purchase_con)	#8
		each.append(i.domain)		#9
		result.append(each)
	user=Info.objects.all().order_by('fan_con')
	users=Follow_user.objects.filter(user_id=request.session['id'])
	follow=[]
	recommend=[]
	for j in users:
		follow.append(j.follow_user_id)
	for u in user:
		if u.user_id in follow:
			pass
		else:
			each=[]
			each.append(u.user_name)		#0
			each.append(u.domain)		#1
			each.append(u.img)			#2
			each.append(u.sign)			#3
			each.append(u.id)			#4
			h=Info.objects.get(user_id=u.user_id)	
			each.append(h.id)			#5
			recommend.append(each)
	return render(request,'courses/courseList.html',{'info':info,'message':mess,'havent':havent,'course':course,'tiny':tiny,'types':types,'result':result,'user1':recommend[0:3],'user2':recommend[4:6]})

def coursecreate(request):
	try:
		tj=time.time()
		policy = qiniu.rs.PutPolicy('mzvideoimg')
		uptoken = policy.token()
		if 'picture' in request.FILES:
			pic=request.FILES['picture']
			suffix=pic.name.split('.')[-1]
			pic=Image.open(pic)
			coordinate=request.POST['coordinate'].split('*')
			region = (int(round(float(coordinate[0]))+1),int(coordinate[1]),int(coordinate[2]),int(coordinate[3]))
			#region=(0,0,100,100)
			cropImg = pic.crop(region)
			#cropImg=pic.thumbnail((int(coordinate[2]),int(coordinate[3])),Image.ANTIALIAS)
			cropImg.save(r"/home/tron/Maizhi/templates/picture/course/"+str(tj)+'.'+suffix)
			#pic.save("/home/tron/Maizhi/templates/picture/course/"+str(tj)+'.'+suffix,suffix)
			#dirs ='templates/picture/course/'+str(tj)
			#if os.path.isfile(dirs):
			#	os.remove(dirs) 
			#fp=open(dirs, 'wb')
			#content=pic.read()
			#fp.write(content)
			#fp.flush()
			#fp.close()
		domain='http://mzvideoimg.qiniudn.com'
		course=Course(name=request.POST['name'],img=str(tj),domain=domain,introduce=request.POST['introduce'],tiny_type_id=request.POST['tiny'],price=request.POST['price'],status=0,over=0,teacher_id=request.session['id'],grade=0)
		course.save()
		qiniu.io.put_file(uptoken,str(tj),r"/home/tron/Maizhi/templates/picture/course/"+str(tj)+'.'+suffix)
		status=course.id
		Post_course(user_id=request.session['id'],post_course_id=course.id,status=1).save()
		return render(request,'courses/success.html',{'status':status})
		#return HttpResponse(str(int(round(float(coordinate[0]))+1))+"---"+str(int(coordinate[1]))+"---"+str(int(coordinate[2]))+"---"+str(int(coordinate[3])))
		#return HttpResponse(coordinate)
	except:
		m=Message.objects.filter(to=request.session['id']).order_by('-time')[0:5]
		info=Info.objects.get(user_id=request.session['id'])
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
		tag=Types.objects.all()
		mycourse=Course.objects.filter(teacher_id=request.session['id']).count()
		return render(request,'courses/courseCreate.html',{'message':mess,'havent':havent,'tag':tag,'info':info,'mycourse':mycourse})
	

def gettiny(request):
	alltiny=Tiny_type.objects.filter(types_id=request.GET['tiny'])
	tiny=[]
	for i in alltiny:
		tiny.append(i.name)
		tiny.append('*')
		tiny.append(i.id)
		tiny.append(',')
	tiny.pop()
	return HttpResponse(tiny)

def changes(request):
	try:
		course=Course.objects.get(id=request.GET['courseid'])
		if 'name' in request.GET:
			course.name=request.GET['name']
		elif 'intro' in request.GET:
			course.introduce=request.GET['intro']
		course.save()
		return HttpResponse('1')
	except:
		return HttpResponse('2')

def finish(request):
	course=Course.objects.get(id=request.GET['course'])
	course.over=1
	course.save()
	return HttpResponse('1')

def thecourse(request,id):
	info=Info.objects.get(user_id=request.session['id'])
	course=Course.objects.get(id=id)
	tiny=Tiny_type.objects.get(id=course.tiny_type_id)
	types=Types.objects.get(id=tiny.types_id)
	tinfo=Info.objects.get(user_id=course.teacher_id)
	f=Follow_user.objects.filter(user_id=request.session['id'])
	follow=[]
	for i in f:
		follow.append(i.follow_user_id)
	if request.session['id']==course.teacher_id:
		focus='3'
	elif course.teacher_id in follow:
		focus='1'
	else:
		focus='0'
	if course.teacher_id==request.session['id']:
		limit='1'
	else:
		user=Purchase.objects.filter(user_id=request.session['id']).filter(status=1)
		own=[]
		for u in user:
			own.append(u.purchase_id)
		if course.id in own:
			limit='2'
		else:
			nopay=Purchase.objects.filter(user_id=request.session['id']).filter(status=2)
			nopaid=[]
			for n in nopay:
				nopaid.append(purchase_id)
			if course.id in nopaid:
				limit='3'
			else:
				limit='4'
	comment=Course_comment.objects.filter(user_id=request.session['id']).filter(course_id=course.id)
	if comment:
		review='1'
	else:
		review='0'
	dis=Course_comment.objects.filter(course_id=course.id)
	discuss=[]
	for d in dis:
		each=[]
		i=Info.objects.get(user_id=d.user_id)
		each.append(i.user_name)      			 #0
		each.append(i.img)			 	 #1
		each.append(d.content)			 #2
		each.append(d.grade)				 #3
		each.append(d.time)				 #4
		each.append(d.id)				 #5
		each.append(i.domain)				 #6
		discuss.append(each)
	lessions=Lession.objects.filter(course_id=course.id)
	#messages.success(request, 'Hello world.')  
	statu=Register.objects.get(id=course.teacher_id)
	purview=''
	if int(statu.status)==int(2):
		purview='1'
	elif int(statu.status)==int(3):
		purview='2'
	fc=Follow_course.objects.filter(user_id=request.session['id']).filter(follow_course_id=course.id)
	collect=''
	if fc:
		collect='1'
	else:
		collect='2'
	return render(request,'courses/theCourse.html',{'info':info,'course':course,'tinfo':tinfo,'limit':limit,'tiny':tiny,'type':types,'focus':focus,'lession':lessions,'discuss':discuss,'review':review,'purview':purview,'collect':collect})

def purchase(request,id):
	course=Course.objects.get(id=id)
	user=Info.objects.get(user_id=course.teacher_id)
	info=Info.objects.get(user_id=request.session['id'])
	return render(request,'courses/purchase.html',{'info':info,'course':course,'user':user})

def addlession(request,id):
	try:
		info=Info.objects.get(user_id=request.session['id'])
		course=Course.objects.get(id=id)
		if 'lessiondoc' in request.FILES:
			policy = qiniu.rs.PutPolicy('mzvideodoc')
			uptoken = policy.token()
			#doc=request.FILES['lessiondoc'].name
			doc=time.time()
			suffix=request.FILES['lessiondoc'].name.split('.')[-1]
			dirs ='templates/doc/'+str(doc)+'.'+suffix
			content = request.FILES['lessiondoc'].read()
			if os.path.isfile(dirs):
				os.remove(dirs) 
			fp=open(dirs, 'wb')
			fp.write(content)
			fp.flush()
			fp.close()
			qiniu.io.put_file(uptoken,str(doc)+'.'+suffix,r"/home/tron/Maizhi/templates/doc/"+str(doc)+'.'+suffix)
		else:
			doc=''
		if 'lessionvideo' in request.FILES:
			policy = qiniu.rs.PutPolicy('mzvideo')
			uptoken = policy.token()
			#video=request.FILES['lessiondoc'].name
			video=time.time()
			suffix=request.FILES['lessionvideo'].name.split('.')[-1]
			dirs ='templates/video/'+str(video)+'.'+suffix
			content = request.FILES['lessionvideo'].read()
			if os.path.isfile(dirs):
				os.remove(dirs) 
			fp=open(dirs, 'wb')
			fp.write(content)
			fp.flush()
			fp.close()
			qiniu.io.put_file(uptoken,str(video)+'.'+suffix,r"/home/tron/Maizhi/templates/video/"+str(video)+'.'+suffix)
		else:
			video=''
		domaindoc="http://mzvideodoc.qiniudn.com"
		domainvideo="http://mzvideo.qiniudn.com"
		result=Lession(course_id=id,name=request.POST['lessionname'],video=domainvideo+str(video)+'.'+suffix,doc=domaindoc+str(doc)+'.'+suffix,lession_no=request.POST['lessionid'])
		result.save()
		return render(request,'courses/addLession.html',{'info':info,'course':course,'result':result.id})
	except:
		info=Info.objects.get(user_id=request.session['id'])
		course=Course.objects.get(id=id)
		return render(request,'courses/addLession.html',{'info':info,'course':course})
	
def buy(request,id):
	course=Course.objects.get(id=id)
	info=Info.objects.get(user_id=request.session['id'])
	if float(request.GET['price'])!=float(course.price):
		return HttpResponse('碧池，滚粗！！！！')
	else:
		Purchase(user_id=request.session['id'],purchase_id=id,teacher_id=course.teacher_id,status=1).save()
		con=int(course.purchase_con)+int(1)
		course.purchase_con=con
		course.save()
		return render(request,'courses/wait.html',{'id':course.id,'info':info})

def comment(request):
	Course_comment(user_id=request.session['id'],course_id=request.GET['course'],content=request.GET['content'],grade=request.GET['star']).save()
	
	return HttpResponse('1')

def collect(request):
	Follow_course(user_id=request.session['id'],follow_course_id=request.GET['course']).save()
	return HttpResponse('1')

def update(request,id):
	course=Course.objects.get(id=id)
	if 'courseImg' in request.FILES:
		image=request.FILES['courseImg']
		filename=course.img
		dirs ='templates/picture/course/'+str(filename)
		content = image.read()
		if os.path.isfile(dirs):
			os.remove(dirs) 
		fp=open(dirs, 'wb')
		fp.write(content)
		fp.flush()
		fp.close()
		course.img=str(filename)
		course.save()
		return render(request,'courses/wait.html',{'id':course.id})
	else:
		return HttpResponse('1')

def play(request,id):
	lession=Lession.objects.get(id=id)
	course=Course.objects.get(id=lession.course_id)
	tiny=Tiny_type.objects.get(id=course.tiny_type_id)
	types=Types.objects.get(id=tiny.types_id)
	info=Info.objects.get(user_id=course.teacher_id)
	statu=Register.objects.get(id=course.teacher_id)
	if request.session['id']!=course.teacher_id:
		past=Purchase.objects.filter(user_id=request.session['id']).get(purchase_id=course.id)
		if past.process=="":
			past.process=str(past.process)+str(lession.id)
		else:
			#lists=past.process.split(',')
			lists=list(past.process)
			if str(lession.id) in lists:
				pass
			else:
				past.process=str(past.process)+str(lession.id)
		past.save()
	else:
		past=""
	purview=''
	if int(statu.status)==int(2):
		purview='1'
	elif int(statu.status)==int(3):
		purview='2'
	
	f=Follow_user.objects.filter(user_id=request.session['id'])
	follow=[]
	for i in f:
		follow.append(i.follow_user_id)
	if request.session['id']==course.teacher_id:
		focus='3'
	elif course.teacher_id in follow:
		focus='1'
	else:
		focus='0'
	lessions=Lession.objects.filter(course_id=course.id)
	if request.session['id']!=course.teacher_id:
		studied=Purchase.objects.filter(user_id=request.session['id']).get(purchase_id=course.id)
		studied=list(studied.process)
		alllessions=[]
		for j in lessions:
			each=[]
			if j.id in studied:
				each.append(1)
			else:
				each.append(0)
			each.append(j.name)
			each.append(studied)
			alllessions.append(each)
	else:
		alllessions=lessions
	return render(request,'courses/play.html',{'lession':lession,'course':course,'tiny':tiny,'types':types,'info':info,'purview':purview,'focus':focus,'alllessions':alllessions})