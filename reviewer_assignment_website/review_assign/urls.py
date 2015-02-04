from django.conf.urls import patterns, include, url
from review_assign import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^ajax-upload$', views.import_uploader, name="my_ajax_upload"),
)