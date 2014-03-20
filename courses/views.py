#encoding:utf-8

from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render
from courses.models import Types,Tiny_type,Course,Lession,Course_comment
from django.utils import timezone
import re,md5,os,time

def types(request):
	return render(request,'courses/types.html')

def tinytypes(request,id):
	return render(request,'courses/tinyTypes.html')

def courselist(request,id):
	return render(request,'courses/tinyTypes.html')

def coursecreate(request,id):
	return render(request,'courses/courseCreate.html')

def thecourse(request,id):
	return render(request,'courses/theCourse.html')

def purchase(request,id):
	return render(request,'courses/purchase.html')

def play(request,id):
	return render(request,'courses/play.html')