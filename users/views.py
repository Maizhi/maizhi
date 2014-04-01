#encoding:utf-8

from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
from groups.models import Group
from login.models import Register
from django import template
from django.views.decorators.csrf import csrf_exempt  
from django.core.urlresolvers import reverse
from django.shortcuts import render
from PIL import Image
#from django.views.decorators.csrf import csrf_protect
from users.models import Info,Teacher,News,Review_of_news,Message,Follow_topic,Follow_user,Follow_group,Follow_course,Post_reward,Post_course,Purchase,Good_news,Good_review_of_news
from django.utils import timezone
import re,md5,os,time,json,base64

def index(request):
	limit = 10
	focus=Follow_user.objects.filter(user_id=request.session['id'])
	fs=[]
	for f in focus:
		fs.append(f.follow_user_id)
	topics = News.objects.filter(user_id__in=fs).order_by('-time')
	paginator = Paginator(topics, limit)
	page = request.GET.get('page')
	try:
	    topics = paginator.page(page)
	except PageNotAnInteger:
	    topics = paginator.page(1)
	except EmptyPage:
	    topics = paginator.page(paginator.num_pages)
	result=[]
	for t in topics:
		each=[]
		i=Info.objects.get(user_id=t.user_id)
		each.append(i.user_name)  #0
		each.append(i.img)        #1
		each.append(t.content)    #2
		each.append(t.time)       #3
		if t.img:
			each.append(t.img)    #4
		else:
			each.append('')       #4
		each.append(t.good_con)   #5
		each.append(t.share_con)  #6
		each.append(t.review_con) #7
		each.append(t.id)         #8
		each.append(i.sign)       #9
		each.append(t.user_id)    #10
		each.append(i.position)   #11
		each.append(i.work)       #12
		result.append(each)
	info=Info.objects.get(user_id=request.session['id'])
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
	return render(request,'users/index.html',{'id':request.session['id'],'info':info,'result':result,'topics':topics,'message':mess,'havent':havent})

@csrf_exempt
def publish(request):
	#try:
		#return HttpResponse(simplejson.loads(str(request.POST)))
		tj=time.time()
		if 'img' in request.POST:
			#u=request.POST['img'].split(',')
			#i=base64.decodestring(u[1])
			files=open("templates/picture/news/"+str(tj), "w")  
			files.write(request.POST['img'].replace('*','+'))
			files.close()
			news=request.POST['news']
			News(user_id=request.session['id'],content=news,good_con=0,share_con=0,review_con=0,img=str(tj)+".jpg").save()
			jpg("templates/picture/news/"+str(tj),"templates/picture/news/"+str(tj)+".jpg")
			return HttpResponse('1')
		else:
			news=request.POST['news']
			News(user_id=request.session['id'],content=news,good_con=0,share_con=0,review_con=0).save()
			return HttpResponse('1')
	#except:
	#	return HttpResponse('0')

def jpg(url,jpg):
	files=open(url)
	fr=files.read()
	frd=fr.split(',')
	decode=base64.decodestring(frd[1])
	files.close()
	f=open(jpg,'w')
	f.write(decode)
	f.close()

def good(request):
	entire=Good_news.objects.filter(news_id=request.GET['newsid'])
	for i in entire:
		if request.session['id']==i.user_id:
			return HttpResponse('2')
	Good_news(news_id=request.GET['newsid'],user_id=request.session['id']).save()
	n=News.objects.get(id=request.GET['newsid'])
	g=int(n.good_con)+int(1)
	n.good_con=g
	n.save()
	return HttpResponse('1')

def message(request):
	realto=News.objects.get(id=request.GET['to'])
	Message(from_id=request.session['id'],to=realto.user_id,content=request.GET['message'],status=1).save()
	return HttpResponse('1')

def share(request):
	try:
		News(user_id=request.session['id'],content=request.GET['sharemsg'],good_con=0,share_con=0,review_con=0,img=request.GET['img']).save()
		oldnews=News.objects.get(id=request.GET['id'])
		oldnews.share_con+=1
		oldnews.save()
		return HttpResponse('OK')
	except:
		return HttpResponse('Wrong')

def head(request):
	info=Info.objects.get(user_id=request.session['id'])
	if 'head' in request.FILES:
		image=request.FILES['head']
		pattern=re.compile(r'\.') 
		head=pattern.split(str(image))
		head[0]=request.session['email']
		filename=head[0]+'.'+head[1]
		dirs ='templates/picture/avatar/'+filename
		content = image.read()
		if os.path.isfile(dirs):
			os.remove(dirs) 
		fp=open(dirs, 'wb')
		fp.write(content)
		fp.flush()
		fp.close()
		info.img=filename
		info.time=timezone.now()
		info.save()
	else:
		image=None
	#return HttpResponse(image)
	return HttpResponseRedirect(reverse('users:setting'))
	#return render(request,"login/home.html")

def getimg(request):
	this=News.objects.get(id=request.GET['imgid'])
	if this.img:
		return HttpResponse(this.img)
	else:
		return HttpResponse('')

def mycourseact(request):
	return render(request,'users/myCourseAct.html')

def home(request,u_id):
	if u_id==request.session['id']:
		identity=1
		info=Info.objects.get(user_id=request.session['id'])
		news=News.objects.filter(user_id=request.session['id']).order_by('-time')
	else:
		identity=0
		info=Info.objects.get(user_id=u_id)
		news=News.objects.filter(user_id=u_id).order_by('-time')
	user=Register.objects.all()[0:5]
	guy=[]
	focus=[]
	f=Follow_user.objects.filter(user_id=request.session['id'])
	for j in f:
		focus.append(j.follow_user_id)
	for u in user:
		if u.id==request.session['id']:
			pass
		elif u.id in focus:
			pass
		else:
			each=[]
			i=Info.objects.get(user_id=u.id)
			each.append(i.user_name)
			each.append(i.sign)
			each.append(i.sex)
			each.append(i.img)
			each.append(i.id)
			guy.append(each)
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
	return render(request,'users/home.html',{'identity':identity,'info':info,'guy':guy,'news':news,'havent':havent})

def add(request):
	f=Follow_user.objects.filter(user_id=request.session['id'])
	follow=[]
	for i in f:
		follow.append(i.follow_user_id)
	if int(request.GET['id']) in follow:
		Follow_user.objects.filter(user_id=request.session['id']).get(follow_user_id=request.GET['id']).delete()
		focus=Info.objects.get(user_id=request.session['id'])
		focus.focus_con-=1
		focus.save()
		fan=Info.objects.get(user_id=request.GET['id'])
		fan.fan_con-=1
		fan.save()
	else:
		Follow_user(user_id=request.session['id'],follow_user_id=request.GET['id']).save()
		focus=Info.objects.get(user_id=request.session['id'])
		focus.focus_con+=1
		focus.save()
		fan=Info.objects.get(user_id=request.GET['id'])
		fan.fan_con+=1
		fan.save()
	return HttpResponse('1')

def managecourse(request):
	return render(request,'users/manageCourse.html')

def managegroup(request):
	follow=Follow_group.objects.filter(user_id=request.session['id'])
	limit=15
	paginator = Paginator(follow, limit)
	page = request.GET.get('page')
	try:
	    follow = paginator.page(page)
	except PageNotAnInteger:
	    follow = paginator.page(1)
	except EmptyPage:
	    follow = paginator.page(paginator.num_pages)
	groups=[]
	for i in follow:
		each=[]
		group=Group.objects.get(id=i.follow_group_id)
		info=Info.objects.get(user_id=group.user_id)
		each.append(group.id)          #0
		each.append(group.name)        #1
		each.append(group.crew_con)    #2
		each.append(info.user_name)    #3
		each.append(info.user_id)      #4
		each.append(group.img)         #5
		groups.append(each)
	my=Group.objects.filter(user_id=request.session['id'])
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
	return render(request,'users/manageGroup.html',{'groups':groups,'follow':follow,'my':my,'message':mess,'havent':havent})

def managereward(request):
	return render(request,'users/managereward.html')

def setting(request):
	info=Info.objects.get(user_id=request.session['id'])
	user=Register.objects.get(id=request.session['id'])
	status=None
	if user.status!="0":
		status=True
	return render(request,'users/setting.html',{'email':request.session['email'],'info':info})

def update(request):
	#try:
		info=Info.objects.get(user_id=request.session['id'])
		info.user_name=request.POST['name']
		info.sex=request.POST['sex']
		info.work=request.POST['work']
		info.position=request.POST['position']
		info.birthday=request.POST['birthday']
		info.constellation=request.POST['constellation']
		info.sign=request.POST['sign']
		info.introduce=request.POST['introduce']
		info.save()
		return HttpResponseRedirect(reverse('users:setting'))
	#except:
	#	return HttpResponse('Login first')

def pwdchange(request):
	user=Register.objects.get(id=request.session['id'])
	old_pwd=request.POST['old_pwd']
	pwd=user.password
	if md5.new(old_pwd).hexdigest()==pwd:
		new_pwd=request.POST['new_pwd']
		if old_pwd!=new_pwd:
			user.password=md5.new(new_pwd).hexdigest()
			user.save()
			return HttpResponseRedirect(reverse('login:index'))
	else:
		return HttpResponse('原密码不正确！')
	

def mytopic(request):
	return render(request,'users/myTopic.html')

def teacherapply(request):
	return render(request,'users/teacherApply.html')
