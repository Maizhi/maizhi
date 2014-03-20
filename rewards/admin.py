from django.contrib import admin
from courses.models import Types
from rewards.models import Reward,Uncover,Reward_mes



class UncoverInline(admin.StackedInline):
	model=Uncover
	extra=0

class Reward_mesInline(admin.StackedInline):
	model=Reward_mes
	extra=0

class RewardAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,{'fields': ['types']}),
		(None,{'fields': ['from_id']}),
		(None,{'fields': ['to']}),
		(None,{'fields': ['message_con']}),
		(None,{'fields': ['uncover_con']}),
		(None,{'fields': ['course_id']}),
		(None,{'fields': ['name']}),
		(None,{'fields': ['introduce']}),
		(None,{'fields': ['price']}),
    	]
	list_display = ('name','types','from_id','to','message_con','uncover_con','course_id','course_id','price')
	search_fields = ['name']
	inlines=[UncoverInline]
	inlines=[Reward_mesInline]

class UncoverAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,{'fields': ['reward']}),
		(None,{'fields': ['to']}),
		(None,{'fields': ['status']}),
    	]
	list_display = ('reward','to','status')
	search_fields = ['to']

class Reward_mesAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,{'fields': ['reward']}),
		(None,{'fields': ['from_id']}),
		(None,{'fields': ['content']}),
    	]
	list_display = ('reward','from_id')

admin.site.register(Reward,RewardAdmin)
admin.site.register(Uncover,UncoverAdmin)
admin.site.register(Reward_mes,Reward_mesAdmin)
