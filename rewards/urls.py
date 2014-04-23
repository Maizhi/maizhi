from django.conf.urls import patterns, url
from rewards import views

urlpatterns = patterns('',
    url(r'^reward/$', views.reward, name="reward"),
    url(r'^rewards/$', views.rewards, name="rewards"),
    url(r'^create/$', views.rewardcreate, name="rewardcreate"),
    url(r'^addReward/$', views.addReward, name="addReward"),
    url(r'^the/(.+)$', views.thereward, name="thereward"),
    url(r'^success/$', views.success, name="success"),
    url(r'^addreview/$', views.addreview, name="addreview"),
    url(r'^uncover/$', views.uncover, name="uncover"),

    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': '/home/sun/Dropbox/mz/templates/public/css' } 
	),
	url(r'^js/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': '/home/sun/Dropbox/mz/templates/public/js' } 
    ),
    url(r'^fonts/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': '/home/sun/Dropbox/mz/templates/public/fonts' } 
    ), 
)
