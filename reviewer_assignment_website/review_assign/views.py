from django.middleware.csrf import get_token
from django.shortcuts import render_to_response
from django.template import RequestContext

from ajaxuploader.views import AjaxFileUploader


def index(request):
    csrf_token = get_token(request)
    return render_to_response('review_assign/index.html',
        {'csrf_token': csrf_token}, context_instance = RequestContext(request))

def result(request):
    csrf_token = get_token(request)
    return render_to_response('review_assign/result.html',
        {'csrf_token': csrf_token}, context_instance = RequestContext(request))

import_uploader = AjaxFileUploader()
