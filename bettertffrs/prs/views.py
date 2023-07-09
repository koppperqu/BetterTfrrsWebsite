from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
# Create your views here.

def athletesearch(request):
    #look at all athletes, look for any that match the search data and return them
    #then display them?
    data=''
    return render(request, 'prs/athletes.html', {'data':data})

def index(request):
    from prs.models import College
    colleges = College.objects.all()
    data=[]
    for college in colleges:
        slug = slugify(college.college_name)
        data.append({'name': college.college_name, 'slug': slug})
    return render(request, 'prs/index.html', {'data':data})

def college(request, college_slug):
    unslugged = college_slug.replace('-', ' ').replace('_', ' ')
    unslugged = unslugged.title()
    data = {"slug":college_slug}
    return render(request, 'prs/college.html', {'data':data})

def athletes(request, college_slug):
    unslugged = college_slug.replace('-', ' ').replace('_', ' ')
    unslugged = unslugged.title()
    from prs.models import College
    from prs.models import Athlete
    college=College.objects.get(college_name=unslugged)
    athletes = Athlete.objects.all().filter(college=college)
    data={"slug":college_slug, "athletes":athletes}
    return render(request, 'prs/athletes.html', {'data':data})

def athlete(request, college_slug, athlete_id):
    from prs.models import Personal_Record
    prs = Personal_Record.objects.all().filter(athlete_id=athlete_id)
    prsAndEventSlugs = []
    for eachPR in prs:
        prsAndEventSlugs.append({"event_slug":slugify(eachPR.event.event_name),"pr":eachPR})
    data = {"college_slug":college_slug, "prsAndEventSlugs":prsAndEventSlugs}
    return render(request, 'prs/athlete.html', {'data':data})

def events(request,college_slug):
    unslugged = college_slug.replace('-', ' ').replace('_', ' ')
    unslugged = unslugged.title()
    from prs.models import College
    from prs.models import Event
    college=College.objects.get(college_name=unslugged)
    events =Event.objects.filter(personal_record__athlete__college=college).distinct()
    eventSlugsAndID = []
    for eachEvent in events:
        eventSlugsAndID.append({"event_slug":slugify(eachEvent.event_name),"event_id":eachEvent.event_id, "name":eachEvent.event_name})
    data={"college_slug":college_slug,"events":eventSlugsAndID}
    return render(request, 'prs/events.html', {'data':data})

def event(request, college_slug, event_slug , id):
    unslugged = college_slug.replace('-', ' ').replace('_', ' ')
    unslugged = unslugged.title()
    from prs.models import Event,Personal_Record
    prs = Personal_Record.objects.filter(event_id=id, athlete__college__college_name=unslugged)
    data = {"prs":prs, "college_slug":college_slug}
    return render(request, 'prs/event.html', {'data':data})