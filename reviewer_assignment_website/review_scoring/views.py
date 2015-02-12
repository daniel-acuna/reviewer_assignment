from django.shortcuts import render, render_to_response
from django.http import HttpResponse

def docs(request):
    return render_to_response('review_scoring/docs_review_scoring.html')
