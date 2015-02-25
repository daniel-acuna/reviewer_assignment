from django.conf.urls import patterns, include, url
from review_assign import views

urlpatterns = patterns('',
    url(r'^$', views.index.as_view(), name='review_assign_index'),
    url(r'^result/(?P<task_id>.+)/$',
        views.result, name='result'),
    url(r'^download_result/(?P<task_id>.+)/$',
        views.download_result, name='download_result'),

    url(r'^docs$', views.docs, name='docs_review_assign'),
)
