from django.conf.urls import patterns, include, url
from review_scoring import views

urlpatterns = patterns('',
    url(r'^docs$', views.docs, name='docs_review_scoring'),
)
