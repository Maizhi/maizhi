from django.conf.urls import patterns, url
from login import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    #url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^addmajor/$', views.addmajor, name='addmajor'),
    url(r'^adduser/$', views.adduser, name='adduser'),
    url(r'^verification/$', views.verification, name='verification'),
    #url(r'^verification/$', views.verification, name='verification'),
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
        { 'document_root': '/home/tron/mz/maizhi/templates/public/img' } 
    ), 
    url(r'^avatar/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': '/home/tron/mz/maizhi/templates/picture/avatar' } 
    ), 
    url(r'^ico/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': '/home/tron/mz/maizhi/templates/picture/ico' } 
    ), 
)
