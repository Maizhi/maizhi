from django.conf.urls import patterns, url
from courses import views

urlpatterns = patterns('',
    url(r'^types/$', views.types, name="types"),
    url(r'^types/gettiny/$', views.gettiny, name="gettiny"),
    url(r'^course/lession/$', views.changes, name="getchangestiny"),
    url(r'^types/tiny/course/lession/add/(.+)$', views.addlession, name="addlession"),
    url(r'^types/tiny/course/purchase/(.+)$', views.purchase, name="purchase"),
    url(r'^types/tiny/course/buy/(.+)$', views.buy, name="buy"),
    url(r'^types/tiny/course/lession/finish/$', views.finish, name="finish"),
    url(r'^types/tiny/course/lession/comment/$', views.comment, name="comment"),
    url(r'^types/tiny/course/lession/collect/$', views.collect, name="collect"),
    url(r'^types/tiny/course/lession/update/(.+)$', views.update, name="update"),
    url(r'^types/tiny/course/lession/(.+)$', views.thecourse, name="thecourse"),
    url(r'^types/tiny/course/play/(.+)$', views.play, name="play"),
    url(r'^types/tiny/course/(.+)$', views.courselist, name="courselist"),
    url(r'^types/tiny/(.+)$', views.tinytypes, name="tinytypes"),
    url(r'^types/create$', views.coursecreate, name="coursecreate"),
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': '/home/tron/mz/maizhi/templates/public/css' } 
    ),
    url(r'^course/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': '/home/tron/mz/maizhi/templates/picture/course' } 
    ),
    url(r'^type/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': '/home/tron/mz/maizhi/templates/picture/type' } 
    ),
    url(r'^tiny/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': '/home/tron/mz/maizhi/templates/picture/tinyType' } 
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
    url(r'^player/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': '/home/tron/Dropbox/mz/templates/public/player' } 
    ), 
)
