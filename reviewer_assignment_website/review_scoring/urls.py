from django.conf.urls import patterns, url
from review_scoring import views

urlpatterns = \
    patterns('',
             url(r'^$', views.Index.as_view(), name='review_scoring_index'),
             url(r'^docs$', views.docs, name='docs_review_scoring'),
             url(r'^result/(?P<task_id>.+)/$',
                 views.result, name='result_scoring'),
             url(r'^download_result/(?P<task_id>.+)/$',
                 views.download_result, name='download_result_scoring'))
