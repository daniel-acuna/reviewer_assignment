from django.conf.urls import patterns, include, url
from review_assign import views

urlpatterns = patterns('',
    url(r'^$', views.index.as_view(), name='review_assign_index'),
    url(r'^create_assignment/(?P<people_fn>.+)/(?P<article_info_fn>.+)/(?P<reviewers_fn>.+)/(?P<coi_fn>.+)/(?P<min_rev_art>.+)/(?P<max_rev_art>.+)/(?P<min_art_rev>.+)/(?P<max_art_rev>.+)/$',
        views.create_assignment, name='create_assignment'),
    url(r'^result/(?P<result_fn>.+)/$',
        views.result, name='result'),
    url(r'^download_result/(?P<result_fn>.+)/$',
        views.download_result, name='download_result'),

    url(r'^docs$', views.docs, name='docs_review_assign'),
)
