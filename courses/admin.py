from django.contrib import admin
from courses.models import Types,Tiny_type,Course,Lession,Course_comment
from rewards.models import Reward

class LessionInline(admin.StackedInline):
	model=Lession
	extra=0

class Course_commentInline(admin.StackedInline):
	model=Course_comment
	extra=0

class CourseInline(admin.StackedInline):
	model=Course
	extra=0

class Tiny_typeInline(admin.StackedInline):
	model=Tiny_type
	extra=0

class RewardInline(admin.StackedInline):
	model=Reward
	extra=0

class TypesAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,{'fields': ['name']}),
		(None,{'fields': ['img']}),
		(None,{'fields': ['big_img']}),
    	]
	list_display = ('name','img')
	search_fields = ['name']
	inlines=[Tiny_typeInline]
	inlines=[RewardInline]

class Tiny_typeAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,{'fields': ['types']}),
		(None,{'fields': ['name']}),
		(None,{'fields': ['introduce']}),
		(None,{'fields': ['img']}),
    	]
	list_display = ('types','name','introduce','img')
	search_fields = ['name']
	inlines=[CourseInline]

class CourseAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,{'fields': ['tiny_type']}),
		(None,{'fields': ['teacher_id']}),
		(None,{'fields': ['name']}),
		(None,{'fields': ['introduce']}),
		(None,{'fields': ['img']}),
		(None,{'fields': ['password']}),
		(None,{'fields': ['price']}),
		(None,{'fields': ['tag']}),
		(None,{'fields': ['grade']}),
		(None,{'fields': ['grade_con']}),
		(None,{'fields': ['purchase_con']}),

		(None,{'fields': ['status']}),
    	]
	list_display = ('tiny_type','name','teacher_id','introduce','price','purchase_con','deadline','status','time')
	search_fields = ['name']
	inlines=[Course_commentInline]
	inlines=[LessionInline]

class LessionAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,{'fields': ['course']}),
		(None,{'fields': ['name']}),
		(None,{'fields': ['video']}),
		(None,{'fields': ['doc']}),
    	]
	list_display = ('course','name','video','doc')
	search_fields = ['name']

admin.site.register(Types,TypesAdmin)
admin.site.register(Tiny_type,Tiny_typeAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(Lession,LessionAdmin)