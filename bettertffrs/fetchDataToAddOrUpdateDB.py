import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
wiacTfrrsURL="https://www.tfrrs.org/leagues/1420.html"
html = urlopen(wiacTfrrsURL)
soup=BeautifulSoup(html.read(), "html.parser")

def getTeamsLinksAndNames(soup):
    teamLinks,teamNames=[],[]
    tableData=soup.find("h3", string="TEAMS").parent.find("table").findAll("a")
    for index,eachTeam in enumerate(tableData):
        if(index%2==0):
            teamLinks.append(eachTeam["href"])
            teamNames.append(eachTeam.text.replace('Wis.-',''))
    return teamLinks, teamNames

def getAthleteLinksAndNames(soup):
    athleteLinksATag = soup.find('h3',string='ROSTER').find_parent().find('tbody').findAll('a')
    athleteNames,athleteLinks=[],[]
    for eachLink in athleteLinksATag:        
        nameParts=eachLink.getText().split(', ')
        athleteNames.append(nameParts[1].strip()+' '+nameParts[0].strip())
        athleteLinks.append('https://www.tfrrs.org'+eachLink['href'])
    return(athleteLinks,athleteNames)

def getTeamsAthleteLinksAndNames(teamLinks):
    teamAthleteLinks, teamAthleteNames = [],[]
    for eachTeam in teamLinks:
        html = urlopen(eachTeam)
        soup=BeautifulSoup(html.read(), "html.parser")
        athleteLinks,athleteNames = getAthleteLinksAndNames(soup)
        teamAthleteLinks.append(athleteLinks)
        teamAthleteNames.append(athleteNames)
    return teamAthleteLinks, teamAthleteNames

def getAthletesEventsAndPRAndPRLink(soup):
    bests=soup.find('table',class_='table bests')#grabs the personal bests table
    bestsTD=bests.findAll('td')
    events=[]
    marks=[]
    prlinks=[]
    for index,each in enumerate(bestsTD):        
        if (each.getText().strip()==''):
            continue
        if index%2==0:
            events.append(each.getText().strip())
        else:
            marks.append(each.find('a').getText().strip())
            prlinks.append(each.find('a')['href'])
    return {"events":events,"marks":marks,"prlinks":prlinks}

def getEachTeamsAthletesEventsAndPRAndPRLink(teamAthleteLinks,teamNames):
    eachTeamsAthletesEventsAndPRAndPRLink=[]
    for teamIndex,eachTeamAthleteLinks in enumerate(teamAthleteLinks):
        currentTeam = teamNames[teamIndex]
        print(f"Current team is {currentTeam} {teamIndex + 1}/{len(teamNames)}")
        allATeamsAthletesData=[]
        for index,eachAthleteLink in enumerate(eachTeamAthleteLinks):
            percent = (index + 1) / len(eachTeamAthleteLinks) * 100
            print(f"Progress: {percent:.2f}%", end="\r")
            html = urlopen(eachAthleteLink)
            soup=BeautifulSoup(html.read(), "html.parser")
            athletesData=getAthletesEventsAndPRAndPRLink(soup)
            allATeamsAthletesData.append(athletesData)
        eachTeamsAthletesEventsAndPRAndPRLink.append(allATeamsAthletesData)
        print()
    return eachTeamsAthletesEventsAndPRAndPRLink

def getTheDataReturnJson():
    teamLinks,teamNames = getTeamsLinksAndNames(soup)
    teamAthleteLinks, teamAthleteNames = getTeamsAthleteLinksAndNames(teamLinks)
    eachTeamsAthletesEventsAndPRAndPRLink = getEachTeamsAthletesEventsAndPRAndPRLink(teamAthleteLinks, teamNames)
    jsonData = {
        "Colleges": []
    }
    for teamIndex, teamName in enumerate(teamNames):
        teamData = {
            "CollegeName": teamName,
            "CollegeLink": teamLinks[teamIndex],
            "Athletes": []
        }
        for athleteIndex, athleteName in enumerate(teamAthleteNames[teamIndex]):
            athleteData = {
                "Name": athleteName,
                "AthletesLink": teamAthleteLinks[teamIndex][athleteIndex],
                "PRS": []
            }
            athletePRData = eachTeamsAthletesEventsAndPRAndPRLink[teamIndex][athleteIndex]
            for event, mark, prlink in zip(athletePRData["events"], athletePRData["marks"], athletePRData["prlinks"]):
                prData = {
                    "EventName": event,
                    "EventMark": mark,
                    "PRLink": prlink
                }
                athleteData["PRS"].append(prData)
            teamData["Athletes"].append(athleteData)
        jsonData["Colleges"].append(teamData)

    json_data = json.dumps(jsonData, indent=4)
    return json_data