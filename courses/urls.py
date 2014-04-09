from django.conf.urls import patterns, url
from courses import views

urlpatterns = patterns('',
    url(r'^types/$', views.types, name="types"),
    url(r'^types/gettiny/$', views.gettiny, name="gettiny"),
    url(r'^course/lession/$', views.changes, name="getchangestiny"),
    url(r'^types/tiny/course/lession/add/(.+)$', views.addlession, name="addlession"),
    url(r'^types/tiny/course/purchase/(.+)$', views.purchase, name="purchase"),
    url(r'^types/tiny/course/buy/(.+)$', views.buy, name="buy"),
    url(r'^types/tiny/course/lession/(.+)$', views.thecourse, name="thecourse"),
    url(r'^types/tiny/course/(.+)$', views.courselist, name="courselist"),
    url(r'^types/tiny/(.+)$', views.tinytypes, name="tinytypes"),
    url(r'^types/tiny/course/play/(.+)$', views.play, name="play"),
    url(r'^types/create$', views.coursecreate, name="coursecreate"),
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
