from django.conf.urls import patterns, url
from groups import views

urlpatterns = patterns('',
    url(r'^$', views.groups, name="groups"),
    url(r'^the/download/down/$', views.down, name="down"),
    url(r'^the/download/(.+)$', views.download, name="download"),
    url(r'^the/upload/(.+)$', views.upload, name="upload"),
    url(r'^the/(.+)$', views.thegroup, name="thegroup"),
    url(r'^change/$', views.change, name="change"),
    url(r'^join/$', views.join, name="join"),
    url(r'^topic/create/(.+)$', views.topiccreate, name="topiccreate"),
    url(r'^topic/publish/$', views.publish, name="publish"),
    url(r'^topic/collect/$', views.collect, name="collect"),
    url(r'^topic/comment/$', views.comment, name="comment"),
    url(r'^topic/good/$', views.good, name="good"),
    url(r'^topic/(.+)$', views.thetopic, name="thetopic"),
    url(r'^create/$', views.groupcreate, name="groupcreate"),

    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': '/home/tron/mz/maizhi/templates/public/css' } 
	),
	url(r'^js/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': '/home/tron/mz/maizhi/templates/public/js' } 
    ),
    url(r'^fonts/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': '/home/tron/mz/maizhi/templates/public/fonts' } 
    ), 
url(r'^img/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': '/home/tron/mz/templates/public/img' } 
    ), 
    url(r'^news/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': '/home/tron/mz/maizhi/templates/picture/news' } 
    ), 
    url(r'^ico/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': '/home/tron/mz/maizhi/templates/picture/ico' } 
    ), 
    url(r'^avatar/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': '/home/tron/mz/maizhi/templates/picture/avatar/' } 
    ), 
    url(r'^group/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': '/home/tron/mz/maizhi/templates/picture/group/image' } 
    ), 
    url(r'^file/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': '/home/tron/mz/maizhi/templates/picture/group/file' } 
    ), 
)
