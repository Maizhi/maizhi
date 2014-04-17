from django.conf.urls import patterns, url
from rewards import views

urlpatterns = patterns('',
    url(r'^$', views.rewards, name="rewards"),
    url(r'^create/$', views.rewardcreate, name="rewardcreate"),
    url(r'^the/(.+)$', views.thereward, name="thereward"),

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
