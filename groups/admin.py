from django.contrib import admin
from groups.models import Group,Topic,Review_of_topic,Good_review_of_topic,Group_file

class TopicInline(admin.StackedInline):
	model=Topic
	extra=0

class Review_of_topicInline(admin.StackedInline):
	model=Review_of_topic
	extra=0

class Good_review_of_topicInline(admin.StackedInline):
	model=Good_review_of_topic
	extra=0

class Group_fileInline(admin.StackedInline):
	model=Group_file
	extra=0



class GroupAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,{'fields': ['tag']}),
		(None,{'fields': ['topic_con']}),
		(None,{'fields': ['filespace']}),
		(None,{'fields': ['user_id']}),
		(None,{'fields': ['introduce']}),
		(None,{'fields': ['img']}),
		(None,{'fields': ['name']}),
		(None,{'fields': ['crew_con']}),
		(None,{'fields': ['status']}),
    	]
	list_display = ('name','tag','topic_con','filespace','user_id','crew_con','status')
	search_fields = ['name']
	inlines=[TopicInline]
	inlines=[Group_fileInline]

class TopicAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,{'fields': ['group']}),
		(None,{'fields': ['user_id']}),
		(None,{'fields': ['share_con']}),
		(None,{'fields': ['collect_con']}),
		(None,{'fields': ['review_con']}),
		(None,{'fields': ['img']}),
		(None,{'fields': ['name']}),
		(None,{'fields': ['content']}),
    	]
	list_display = ('name','user_id','share_con','collect_con','review_con')
	search_fields = ['name']
	inlines=[Review_of_topicInline]

class Review_of_topicAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,{'fields': ['topic']}),
		(None,{'fields': ['from_id']}),
		(None,{'fields': ['to']}),
		(None,{'fields': ['content']}),
		(None,{'fields': ['good_con']}),
		(None,{'fields': ['review_con']}),
		(None,{'fields': ['to_review']}),
    	]
	list_display = ('topic','from_id','to','good_con','review_con')
	search_fields = ['to']
	inlines=[Good_review_of_topicInline]

class Good_review_of_topicAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,{'fields': ['review_of_topic']}),
		(None,{'fields': ['user_id']}),
    	]
	list_display = ('user_id','review_of_topic')
	search_fields = ['review_of_topic']

class Group_fileAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,{'fields': ['group']}),
		(None,{'fields': ['user_id']}),
		(None,{'fields': ['name']}),
		(None,{'fields': ['introduce']}),
		(None,{'fields': ['file_path']}),
		(None,{'fields': ['down_con']}),
    	]
	list_display = ('user_id','name')
	search_fields = ['name']

admin.site.register(Group,GroupAdmin)
admin.site.register(Topic,TopicAdmin)
admin.site.register(Review_of_topic,Review_of_topicAdmin)
admin.site.register(Good_review_of_topic,Good_review_of_topicAdmin)
admin.site.register(Group_file,Group_fileAdmin)