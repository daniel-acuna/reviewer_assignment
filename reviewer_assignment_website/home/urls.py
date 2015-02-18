from django.conf.urls import patterns, include, url
from home import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^docs/', views.docs, name='docs_home'),
    url(r'^cancel_task/(?P<task_id>.+)/(?P<redirect_url>.+)/$', views.cancel_task,
        name='cancel_task'),
)
