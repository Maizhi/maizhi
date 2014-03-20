#encoding:utf-8

from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render
from rewards.models import Reward,Uncover,Reward_mes
from django.utils import timezone
import re,md5,os,time

def rewards(request):
	return render(request,'rewards/rewards.html')

def rewardcreate(request):
	return render(request,'rewards/rewardCreate.html')

def thereward(request,id):
	return render(request,'rewards/theReward.html')



