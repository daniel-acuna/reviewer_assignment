from django.shortcuts import render, render_to_response
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render_to_response('home/index.html')