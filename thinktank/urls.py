from django.conf.urls import patterns, include, url
from django.contrib import admin
from t3manager import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login
#from django.conf.urls.defaults import *
from django.contrib.auth.views import password_change

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^importCSV$', views.importCSV, name='importCSV'),
    url(r'^member/(?P<member_id>\d+)/view$', views.viewMember, name='viewMember'),
    url(r'^project/(?P<project_id>\d+)/view$', views.viewProject, name='viewProject'),
    url(r'^project/(?P<project_id>\d+)/updateMembers/(?P<profile_id>\d+)/(?P<command>\S+)$', views.updateMembers, name='updateMembers'),
    url(r'^project/(?P<pk>\d+)/edit$', views.editProject.as_view(), name='editProject'),
    url(r'^filterMembers/$', views.filterMembers, name='filterMembers'),
    url(r'^showProjects/$', views.showProjectOverview, name='showProjectOverview'),
    url(r'^editProfile/$', views.editProfile, name='editProfile'),
    url(r'^updateProfile/$', views.updateProfile, name='updateProfile'),
    url(r'^changePassword/$', password_change, {'template_name': 'password_reset.html', 'post_change_redirect':'/'}),
    url(r'^password_change_done/$', 'django.contrib.auth.views.password_change_done'),

    url(r'^$', views.frontpage, name='frontpage'),

    #may not longer be supoorted
    url(r'^member/(?P<pk>\d+)/edit$', views.editMember.as_view(), name='editMember'),


    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^accounts/(?P<user_id>\d+)/$', login_required(views.userDetails), name='userDetail'),
    url(r'^accounts/login', login, {'template_name': 'login.html'}),
    url(r'^accounts/logout', 'django.contrib.auth.views.logout', {'template_name': 'login.html'}),
)
