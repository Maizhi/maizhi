from django.contrib import admin
from users.models import Info,Teacher,News,Review_of_news,Message,Follow_topic,Follow_user,Follow_group,Follow_course,Post_reward,Post_course,Purchase,Good_news,Good_review_of_news

class Review_of_newsInline(admin.StackedInline):
	model=Review_of_news
	extra=0

class Good_newsInline(admin.StackedInline):
	model=Good_news
	extra=0

class Good_review_of_newsInline(admin.StackedInline):
	model=Good_review_of_news
	extra=0

class InfoAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,{'fields': ['user']}),
		(None,{'fields': ['user_name']}),
		(None,{'fields': ['work']}),
		(None,{'fields': ['position']}),
		(None,{'fields': ['introduce']}),
		(None,{'fields': ['sign']}),
		(None,{'fields': ['birthday']}),
		(None,{'fields': ['sex']}),
		(None,{'fields': ['img']}),
		(None,{'fields': ['follow_group_con']}),
		(None,{'fields': ['fan_con']}),
		(None,{'fields': ['focus_con']}),
		(None,{'fields': ['constellation']}),
		(None,{'fields': ['tag']}),
		(None,{'fields': ['credit']}),
    	]
	list_display = ('user_name','sex','follow_group_con','fan_con','focus_con','credit')
	search_fields = ['user_name']

class TeacherAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,{'fields': ['user']}),
		(None,{'fields': ['real_name']}),
		(None,{'fields': ['alipay']}),
		(None,{'fields': ['identity']}),
		(None,{'fields': ['tel']}),
		(None,{'fields': ['identity_img']}),
    	]
	list_display = ('user','real_name')
	search_fields = ['user']

class NewsAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,{'fields': ['user']}),
		(None,{'fields': ['content']}),
		(None,{'fields': ['good_con']}),
		(None,{'fields': ['share_con']}),
		(None,{'fields': ['review_con']}),
		(None,{'fields': ['img']}),
    	]
	list_display = ('good_con','share_con','review_con')
	search_fields = ['user']
	inlines=[Review_of_newsInline]

class Review_of_newsAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,{'fields': ['news']}),
		(None,{'fields': ['content']}),
		(None,{'fields': ['from_id']}),
		(None,{'fields': ['to']}),
		(None,{'fields': ['good_con']}),
    	]
	list_display = ('news','from_id','to','good_con')
	search_fields = ['news']

class MessageAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,{'fields': ['status']}),
		(None,{'fields': ['from_id']}),
		(None,{'fields': ['to']}),
		(None,{'fields': ['content']}),
    	]
	list_display = ('status','from_id','to')

class Follow_userAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,{'fields': ['user']}),
		(None,{'fields': ['follow_user_id']}),
    	]
	list_display = ('user','follow_user_id')

class Follow_topicAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,{'fields': ['user']}),
		(None,{'fields': ['follow_topic_id']}),
    	]
	list_display = ('user','follow_topic_id')

class Follow_groupAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,{'fields': ['user']}),
		(None,{'fields': ['follow_group_id']}),
		(None,{'fields': ['topic_con']}),
		(None,{'fields': ['good_con']}),
		(None,{'fields': ['review_con']}),
		(None,{'fields': ['file_con']}),
		(None,{'fields': ['status']}),
    	]
	list_display = ('user','follow_group_id','topic_con','good_con','review_con','file_con','status')

class Follow_courseAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,{'fields': ['user']}),
		(None,{'fields': ['follow_course_id']}),
    	]
	list_display = ('user','follow_course_id')

class Post_rewardAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,{'fields': ['user']}),
		(None,{'fields': ['uncover']}),
		(None,{'fields': ['post_reward_id']}),
		(None,{'fields': ['status']}),
    	]
	list_display = ('user','post_reward_id','status')

class Post_courseAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,{'fields': ['user']}),
		(None,{'fields': ['post_course_id']}),
		(None,{'fields': ['status']}),
    	]
	list_display = ('user','post_course_id','status')

class PurchaseAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,{'fields': ['user']}),
		(None,{'fields': ['purchase_id']}),
		(None,{'fields': ['teacher_id']}),
		(None,{'fields': ['process']}),
    	]
	list_display = ('user','purchase_id','process')

class Good_newsAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,{'fields': ['news']}),
		(None,{'fields': ['user_id']}),
    	]
	list_display = ('news','user_id')

class Good_review_of_newsAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,{'fields': ['review_of_news']}),
		(None,{'fields': ['user_id']}),
    	]
	list_display = ('review_of_news','user_id')



admin.site.register(Info,InfoAdmin)
admin.site.register(Teacher,TeacherAdmin)
admin.site.register(News,NewsAdmin)
admin.site.register(Review_of_news,Review_of_newsAdmin)
admin.site.register(Message,MessageAdmin)
admin.site.register(Follow_topic,Follow_topicAdmin)
admin.site.register(Follow_user,Follow_userAdmin)
admin.site.register(Follow_group,Follow_groupAdmin)
admin.site.register(Follow_course,Follow_courseAdmin)
admin.site.register(Post_reward,Post_rewardAdmin)
admin.site.register(Post_course,Post_courseAdmin)
admin.site.register(Purchase,PurchaseAdmin)
admin.site.register(Good_news,Good_newsAdmin)
admin.site.register(Good_review_of_news,Good_review_of_newsAdmin)
