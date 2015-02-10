from django.conf.urls import patterns, include, url
from review_assign import views

urlpatterns = patterns('',
    url(r'^$', views.index.as_view(), name='review_assign_index'),
    url(r'^result/(?P<people_fn>.+)/(?P<article_info_fn>.+)/(?P<reviewers_fn>.+)/(?P<coi_fn>.+)/(?P<min_rev_art>.+)/(?P<max_rev_art>.+)/(?P<min_art_rev>.+)/(?P<max_art_rev>.+)/$',
        views.result, name='result'),
    url(r'^ajax-upload$', views.import_uploader, name="my_ajax_upload"),
)