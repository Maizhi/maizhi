#encoding:utf-8

from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from login.models import Register
from users.models import Info,Follow_user
from django.utils import timezone
from email.mime.text import MIMEText
import re,md5,smtplib,base64,os

def index(request):
	return render(request,'login/login.html')

def login(request):
	try:
		email=request.GET['email2']
		pwd=md5.new(request.GET['password2']).hexdigest()
		#match=re.search(r"([+-.?$%()<>].*)",user_account)
		#if match:
		#	return HttpResponse('Your account was illegal !')
		#if re.match(r"\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*",user_account):
		user=Register.objects.get(email=email)
		if pwd==user.password:
			request.session['email']=email
			request.session['id']=user.id
			name=Info.objects.get(user_id=user.id).user_name
			request.session['name']=name
			return HttpResponse(user.id)
		else:
			return HttpResponse('密码错误 !')
		#else:
		#	user=Register.objects.get(account=user_account)
		#	if user_password==user.password:
		#		request.session['user']=user_account
		#		return HttpResponse('You are login !')
		#	else:
		#		return HttpResponse('密码错误 !')
	except:
		return HttpResponse('用户不存在!')

def register(request):
	try:
		#account=request.GET['account']
		email=request.GET['email']
		#match=re.search(r"([+-.?*#/$%()<>].*)",account)
		#if len(account)<4:
		#	return HttpResponse('用户名过短!')
		#if match:
		#	return HttpResponse('非法的用户名 !')
		if Register.objects.filter(email=email):
			return HttpResponse('邮箱已注册!')
		else:
			password=md5.new(request.GET['password']).hexdigest()
			if re.match(r"\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*",email):
				s=Register(password=password,email=email)
				s.save()
				mail(email)
				i=Info(user_id=s.id,user_name=request.GET['name'],img='default.png')
				#Follow_user(user_id=s.id,follow_user_id=s.id()).save()
				i.save()
				#return render(request,'login/home.html',{'email':email,'status':0})
				request.session['email']=email
				request.session['id']=s.id
				request.session['name']=request.GET['name']
				return HttpResponse(s.id)
			else:
				return HttpResponse('邮箱格式不正确!')
	except:
		#account=request.GET['account'].encode("utf-8")
		return HttpResponse("服务器崩溃 !")

def verification(request):
	try:
		key=request.GET['key']
		email=base64.decodestring(key)
		user=Register.objects.get(email=email)
		user.status=2
		user.save()
		return HttpResponse("邮箱通过验证")
		#return render(request,'login/home.html',{'email':email,'status':"邮箱通过验证"})
	except:
		return HttpResponse(' 服务器崩溃 !')

def addmajor(request):
	return render(request,'login/add.html',{'name':request.session['name']})

def adduser(request):
	recommend=Register.objects.filter(status==2).order_by('?')[0:20]
	show=[]
	for i in recommend:
		info=Info.objects.get(user_id=i.id)
		show.append(info)
	return render(request,'login/user.html',{'name':request.session['name'],'show':show})

def mail(address):
	mailto_list=address
	mail_host="smtp.126.com"
	mail_name="麦知网"
	mail_user="moutain1"
	mail_pass="Michael29j"
	mail_postfix="126.com"
	me=mail_name+"<"+mail_user+"@"+mail_postfix+">"
	content="http://192.168.1.113:8866/verification/?key="+base64.encodestring(address)+"\nWelcome To Join Us !\n"
	msg = MIMEText(content)
	msg['Subject'] = '麦知网确认邮件!'
	msg['From'] = me
	msg['To'] = mailto_list
	try:
	    s = smtplib.SMTP()
	    s.connect(mail_host)
	    s.login(mail_user,mail_pass)
	    s.sendmail(me, mailto_list, msg.as_string())
	    s.close()
	    return 'OK !'
	except Exception, e:
	    #print str(e)
	    return 'False !'