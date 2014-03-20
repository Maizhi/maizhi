from django.conf.urls import patterns, url
from courses import views

urlpatterns = patterns('',
    url(r'^types/$', views.types, name="types"),
    url(r'^types/tiny/(.+)$', views.tinytypes, name="tinytypes"),
    url(r'^types/tiny/courses/(.+)$', views.courselist, name="courselist"),
    url(r'^types/tiny/courses/lession/(.+)$', views.thecourse, name="thecourse"),
    url(r'^types/tiny/courses/purchase/(.+)$', views.purchase, name="purchase"),
    url(r'^types/tiny/courses/play/(.+)$', views.play, name="play"),
    url(r'^types/create$', views.coursecreate, name="coursecreate"),
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': '/home/tron/Python/code/django/worksys/templates/public/css' } 
	),
	url(r'^js/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': '/home/tron/Python/code/django/worksys/templates/public/js' } 
    ),
    url(r'^fonts/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': '/home/tron/Python/code/django/worksys/templates/public/fonts' } 
    ), 
    url(r'^img/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': '/home/tron/mz/templates/public/img' } 
    ), 
)
