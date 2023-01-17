from django.shortcuts import render
from django.http import HttpResponse, Http404

# Create your views here.

def index(request):
    return render(request, "prs/index.html")

def recentprs(request):
    return HttpResponse("Your looking at RECENT PRS")

def athlete(request, athlete_id):
    return HttpResponse("Your looking at athlete with id %s." %athlete_id)

def event(request, event_id):
    return HttpResponse("Your looking at event with id %s." %event_id)