from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mz.views.home', name='home'),
    # url(r'^mz/', include('mz.foo.urls')),
    url(r'^',include('login.urls',namespace='login')),
    url(r'^users/',include('users.urls',namespace='users')),
    url(r'^courses/',include('courses.urls',namespace='courses')),
    url(r'^groups/',include('groups.urls',namespace='groups')),
    url(r'^rewards/',include('rewards.urls',namespace='rewards')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
