from django.shortcuts import render
from django.http import HttpResponse, Http404
# Create your views here.

def index(request):
    import json  
    f = open('recentPRs.json')
    data = json.load(f)
    f.close()
    return render(request, 'prs/recentPRs.html', {'data':data})


def athletes(request):
    from prs.models import Athlete
    data = Athlete.objects.all().order_by('athlete_name')
    return render(request, 'prs/athletes.html', {'data':data})

def athlete(request, athlete_id):
    from prs.models import Athlete,Personal_Record
    data = Personal_Record.objects.all().filter(athlete_id=athlete_id)
    return render(request, 'prs/athlete.html', {'data':data})

def event(request, id):
    from prs.models import Event,Personal_Record
    data = Personal_Record.objects.all().filter(event_id=id)
    return render(request, 'prs/event.html', {'data':data})

def events(request):
    from prs.models import Event
    data = Event.objects.all()
    return render(request, 'prs/events.html', {'data':data})