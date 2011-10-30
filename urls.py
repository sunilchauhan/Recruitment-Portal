from django.conf.urls.defaults import patterns, include
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^recruit/',include('portal.recruitment.urls')),
    (r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
    (r'^$','django.contrib.auth.views.login'),
    ('^logout/$', 'django.contrib.auth.views.logout'),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^home/$','recruitment.views.baseview'),
)
