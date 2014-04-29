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
from django.contrib import messages
#from django.views.decorators.csrf import csrf_protect
from users.models import Info,Teacher,News,Review_of_news,Message,Follow_topic,Follow_user,Follow_group,Follow_course,Post_reward,Post_course,Purchase,Good_news,Good_review_of_news
from django.utils import timezone
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re,md5,os,time,json,base64,qiniu.io,qiniu.conf,qiniu.rs

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
		if t.src:
			each.append(t.src)    #4
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
		re_of_news=Review_of_news.objects.filter(news_id=t.id).order_by('-time')[0:1]
		for r in re_of_news:
			each.append(r.id)			#13	
			each.append(r.content)		#14	
			info=Info.objects.get(user_id=r.from_id)
			each.append(info.user_name)	#15	
			each.append(info.img)		#16
			each.append(r.to)			#17
			each.append(r.good_con)	 	#18
			each.append(r.time)		 	#19
			each.append(r.review_con)	#20
			each.append(r.from_id)		#21
			each.append(info.domain)			#22
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
	statu=Register.objects.get(id=request.session['id'])
	purview=''
	if int(statu.status)==int(2):
		purview='1'
	elif int(statu.status)==int(3):
		purview='2'
	return render(request,'users/index.html',{'purview':purview,'id':request.session['id'],'info':info,'result':result,'topics':topics,'message':mess,'havent':havent})

@csrf_exempt
def publish(request):
	#try:
		policy = qiniu.rs.PutPolicy('mzimage')
		uptoken = policy.token()
		tj=time.time()
		if 'img' in request.POST:
			#u=request.POST['img'].split(',')
			#i=base64.decodestring(u[1])
			#suffix=request.POST['img'].name.split('.')[-1]
			dirs="templates/picture/news/"+str(tj)
			files=open("templates/picture/news/"+str(tj), "w")  
			files.write(request.POST['img'].replace('*','+'))
			files.close()
			news=request.POST['news']
			domain='http://mzimage.qiniudn.com'
			News(user_id=request.session['id'],src=domain+'/'+str(tj),content=news,good_con=0,share_con=0,review_con=0,img=str(tj)).save()
			jpg("templates/picture/news/"+str(tj),"templates/picture/news/"+str(tj))
			ret=qiniu.io.put_file(uptoken,str(tj),r"/home/tron/Maizhi/templates/picture/news/"+str(tj))
			if ret:
				os.remove(dirs)
			return HttpResponse('1')
		else:
			news=request.POST['news']
			News(user_id=request.session['id'],content=news,good_con=0,share_con=0,review_con=0,img="").save()
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
	policy = qiniu.rs.PutPolicy('mzhead')
	uptoken = policy.token()
	if 'picture' in request.FILES:
		tj=time.time()
		pic=request.FILES['picture']
		suffix=pic.name.split('.')[-1]
		pic=Image.open(pic)
		coordinate=request.POST['coordinate'].split('*')
		region = (int(round(float(coordinate[0]))+1),int(coordinate[1]),int(coordinate[2]),int(coordinate[3]))
		#region=(0,0,100,100)
		cropImg = pic.crop(region)
		#cropImg=pic.thumbnail((int(coordinate[2]),int(coordinate[3])),Image.ANTIALIAS)
		cropImg.save(r"/home/tron/Maizhi/templates/picture/avatar/"+str(tj)+'.'+suffix)
		domain="http://mzhead.qiniudn.com"
		#dirs ='templates/picture/avatar/'+str(tj)
		#if os.path.isfile(dirs):
		#	os.remove(dirs) 
		#fp=open(dirs, 'wb')
		#content=pic.read()
		#fp.write(content)
		#fp.flush()
		#fp.close()
		ret=qiniu.io.put_file(uptoken,str(tj),r"/home/tron/Maizhi/templates/picture/avatar/"+str(tj)+'.'+suffix)
		#if ret:
		#	os.remove(dirs)
		info.img=str(tj)
		info.domain=domain
		info.time=timezone.now()
		info.save()
	#return HttpResponse(image)
	messages.add_message(request, messages.SUCCESS, '修改成功！') 
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
	info=Info.objects.get(user_id=request.session['id'])
	if int(u_id)==int(request.session['id']):
		identity='1'
		userinfo=Info.objects.get(user_id=request.session['id'])
		news=News.objects.filter(user_id=request.session['id']).order_by('-time')
	else:
		identity='0'
		userinfo=Info.objects.get(user_id=u_id)
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
			each.append(i.user_name)		#0
			each.append(i.sign)				#1
			each.append(i.sex)				#2
			each.append(i.img)				#3
			each.append(i.id)				#4
			each.append(i.domain)			#5
			guy.append(each)
	my=Group.objects.filter(user_id=request.session['id'])
	fg=Follow_group.objects.filter(user_id=request.session['id'])
	fogo=[]
	follow=[]
	for l in fg:
		follow.append(l.follow_group_id)
		g=Group.objects.get(id=l.follow_group_id)
		each=[]
		each.append(g.name)
		each.append(g.domain)
		each.append(g.img)
		each.append(g.domain)
		fogo.append(each)
	mygroup=[]
	for k in my:
		each=[]
		each.append(k.name)			#0
		each.append(k.domain)		#1
		each.append(k.img)			#2
		each.append(k.introduce)		#3
		if k.id in follow:
			each.append('1')		#4
		else:
			each.append('0')		#4
		each.append(k.id)			#5
		#Topic.objects.filter(group_id=k.id).order_by('-review_con')[0:3]
		mygroup.append(each)
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
	return render(request,'users/home.html',{'mygroup':mygroup,'identity':identity,'userinfo':userinfo,'info':info,'guy':guy,'news':news,'havent':havent,'fg1':fogo[0:6],'fg2':fogo[7:12]})

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
	info=Info.objects.get(user_id=request.session['id'])
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
		k=Info.objects.get(user_id=group.user_id)
		each.append(group.id)          #0
		each.append(group.name)        #1
		each.append(group.crew_con)    #2
		each.append(k.user_name)    #3
		each.append(k.user_id)      #4
		each.append(group.img)         #5
		each.append(group.domain)      #6
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
	return render(request,'users/manageGroup.html',{'groups':groups,'follow':follow,'my':my,'message':mess,'havent':havent,'info':info})

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
		messages.add_message(request, messages.SUCCESS, '修改成功！') 
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

def comment(request):
	news_id=request.GET['news_id']
	content=request.GET['content']
	from_id=request.session['id']
	newsTable=News.objects.get(id=news_id)
	to=newsTable.user_id
	good_con=0
	time=timezone.now()
	re_of_news=Review_of_news(news_id=news_id,content=content,from_id=from_id,to=to,good_con=good_con,time=time)
	re_of_news.save()
	re_news_id=re_of_news.id
	newsTable.review_con=int(newsTable.review_con)+1
	newsTable.save()
	info=Info.objects.get(user_id=from_id)
	strr=str(re_news_id)+','+str(news_id)+','+str(content)+','+str(from_id)+','+str(info.user_name)+','+str(info.img)+','+str(good_con)+','+str(re_of_news.review_con)+','+str(to)
			#0					#1  			#2 				#3 							#4 				#5						#6			#7							#8
	return HttpResponse(strr)
	
def cocomment(request):
	news_id=request.GET['news_id']
	content=request.GET['content']
	re_id=request.GET['re_id']
	to=request.GET['to']
	from_id=request.session['id']	
	good_con=0
	time=timezone.now()
	re_of_news=Review_of_news(news_id=news_id,content=content,from_id=from_id,to=to,good_con=good_con,time=time)
	re_of_news.save()
	re_news_id=re_of_news.id
	newsTable=News.objects.get(id=news_id)
	newsTable.review_con=int(newsTable.review_con)+1
	newsTable.save()
	beihuifu_re=Review_of_news.objects.get(id=re_id)
	beihuifu_re.review_con=int(beihuifu_re.review_con)+1
	beihuifu_re.save()
	info=Info.objects.get(user_id=from_id)
	strr=str(re_news_id)+','+str(news_id)+','+str(content)+','+str(from_id)+','+str(info.user_name)+','+str(info.img)+','+str(good_con)+','+str(re_of_news.review_con)+','+str(to)
			#0					#1  			#2 				#3 							#4 				#5						#6			#7							#8
	return HttpResponse(strr)	


def get_more_re(request):
	news_id=request.GET['news_id']
	re_of_news=Review_of_news.objects.filter(news_id=news_id).order_by('time')
	strr=''
	for r in re_of_news:
		info=Info.objects.get(user_id=r.from_id)
		strr+=str(r.id)+','+str(news_id)+','+str(r.content)+','+str(r.from_id)+','+str(info.user_name)+','+str(info.img)+','+str(r.good_con)+','+str(r.review_con)+','+str(r.to)+','+str(r.time)+'*'
				#0				#1 				#2 				#3 					#4 						#5					#6					#7 					#8 				#9
	return HttpResponse(strr)

def cogood(request):
	entire=Good_review_of_news.objects.filter(review_of_news_id=request.GET['reviewOfNews_id'])
	for i in entire:
		if request.session['id']==i.user_id:
			return HttpResponse('2')
	Good_review_of_news(review_of_news_id=request.GET['reviewOfNews_id'],user_id=request.session['id']).save()
	n=Review_of_news.objects.get(id=request.GET['reviewOfNews_id'])
	g=int(n.good_con)+int(1)
	n.good_con=g
	n.save()
	return HttpResponse('1')

def message(request):
	realto=News.objects.get(id=request.GET['to'])
	Message(from_id=request.session['id'],to=realto.user_id,content=request.GET['message'],status=1).save()
	return HttpResponse('1')

def mytopic(request):
	return render(request,'users/myTopic.html')

def teacherapply(request):
	return render(request,'users/teacherApply.html')
