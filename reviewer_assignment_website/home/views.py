from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from reviewer_assignment_website import celery_app


def index(_):
    return render_to_response('home/index.html')


def docs(_):
    return render_to_response('home/docs_home.html')


def about(_):
    return render_to_response('home/about.html')


def cancel_task(_, task_id=None, redirect_url=None):
    """Cancels a celery tasks and redirects browser to given URL"""
    print "Cancelling task %s" % task_id
    celery_app.control.revoke(task_id, terminate=True)

    return HttpResponseRedirect(reverse(redirect_url))
