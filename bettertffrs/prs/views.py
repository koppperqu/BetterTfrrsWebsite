from django.shortcuts import render
from django.http import HttpResponse, Http404
from datetime import datetime,timedelta
import GetLast2WeeksPRs
# Create your views here.
lastRanDate=datetime.today().date()

def index(request):
    global lastRanDate
    today = datetime.today().date()
    tdelta=today-lastRanDate
    if (tdelta.days>=1):
        GetLast2WeeksPRs.getLast2WeeksPRs()
        lastRanDate=today
    import json  
    f = open('recentPRs.json')
    data = json.load(f)
    f.close()
    for eachMeet in data:
        countToX=0
        replacePrsAtMeet=[]
        rowsOfZ=[]
        holdX=[]
        counttoZ=0
        for eachPR in eachMeet['prsatmeet']:
            if(countToX==10):
                rowsOfZ.append(holdX)
                holdX=[]
                counttoZ+=1
                countToX=0
                if(counttoZ==2):
                    replacePrsAtMeet.append(rowsOfZ)
                    rowsOfZ=[]
                    counttoZ=0
            holdX.append(eachPR)
            countToX+=1
        if(holdX!=[]):
                rowsOfZ.append(holdX)
        if(rowsOfZ!=[]):
            replacePrsAtMeet.append(rowsOfZ)
        eachMeet['prsatmeet']=replacePrsAtMeet
    return render(request, 'prs/index.html', {'data':data})


def athlete(request, athlete_id):
    return HttpResponse("Your looking at athlete with id %s." %athlete_id)

def event(request, event_id):
    return HttpResponse("Your looking at event with id %s." %event_id)