from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^assignment/', include('review_assign.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('home.urls')),
)
