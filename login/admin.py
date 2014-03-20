from django.contrib import admin
from login.models import Register
from users.models import Info,Teacher,News,Follow_user,Follow_group,Follow_course,Post_reward,Post_course,Purchase

class InfoInline(admin.StackedInline):
	model=Info
	extra=0

class TeacherInline(admin.StackedInline):
	model=Teacher
	extra=0

class NewsInline(admin.StackedInline):
	model=News
	extra=0

class Follow_userInline(admin.StackedInline):
	model=Follow_user
	extra=0

class Follow_groupInline(admin.StackedInline):
	model=Follow_group
	extra=0
	
class Follow_courseInline(admin.StackedInline):
	model=Follow_course
	extra=0

class Post_rewardInline(admin.StackedInline):
	model=Post_reward
	extra=0
		
class Post_courseInline(admin.StackedInline):
	model=Post_course
	extra=0

class PurchaseInline(admin.StackedInline):
	model=Purchase
	extra=0

class RegisterAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,{'fields': ['email']}),
		(None,{'fields': ['password']}),
		(None,{'fields': ['status']}),
    	]
	list_display = ('email','password','status')
	search_fields = ['email']

admin.site.register(Register,RegisterAdmin)