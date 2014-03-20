from django.conf.urls import patterns, url
from groups import views

urlpatterns = patterns('',
    url(r'^$', views.groups, name="groups"),
    url(r'^the/(.+)$', views.thegroup, name="thegroup"),
    url(r'^topic/create/(.+)$', views.topiccreate, name="topiccreate"),
    url(r'^topic/(.+)$', views.thetopic, name="thetopic"),
    url(r'^create/$', views.groupcreate, name="groupcreate"),

    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': '/home/tron/Dropbox/mz/templates/public/css' } 
	),
	url(r'^js/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': '/home/tron/Dropbox/mz/templates/public/js' } 
    ),
    url(r'^fonts/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': '/home/tron/Dropbox/mz/templates/public/fonts' } 
    ), 
)