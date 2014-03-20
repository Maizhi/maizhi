#encoding:utf-8

from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render
from groups.models import Group,Topic,Review_of_topic,Good_review_of_topic,Group_file
from django.utils import timezone
import re,md5,os,time

def groups(request):
	return render(request,'groups/groups.html')

def thegroup(request,id):
	return render(request,'groups/theGroup.html')

def topiccreate(request,id):
	return render(request,'groups/topicCreate.html')

def thetopic(request,id):
	return render(request,'groups/theTopic.html')

def groupcreate(request):
	return render(request,'groups/groupCreate.html')

