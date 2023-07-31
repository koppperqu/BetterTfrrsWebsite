from datetime import datetime
from itertools import groupby
from fetchDataToAddOrUpdateDB import *
from django.utils.text import slugify

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
wiacTfrrsURL="https://www.tfrrs.org/leagues/1420.html"

def getTeamsLastXMeets(soup, numberOfMeets=2):
    latestResultsAnchorTags = soup.find('h3',string='LATEST RESULTS').find_parent().find_parent().find('tbody').find_all('a')
    lastXMeets = []
    for x in range(numberOfMeets):
        lastXMeets.append(latestResultsAnchorTags[x]['href'])
    return lastXMeets

def getAthletesLastXMeets(soup, numberOfMeets=2):
    recentMeetsForAthlete = soup.find('div',id='meet-results').find_all('table')
    recentMeetURLs=[]
    recentMeets = []
    if(len(recentMeetsForAthlete)<numberOfMeets):
        numberOfMeets=len(recentMeetsForAthlete)
    for x in range(numberOfMeets):
        recentMeets.append(recentMeetsForAthlete[x])
        recentMeetURLs.append(recentMeetsForAthlete[x].find('thead').find('a')['href'])
    return recentMeetURLs,recentMeets

def getAllTeamsLast2WeeksPrsPutInJSONFormat():
    html = urlopen(wiacTfrrsURL)
    soup=BeautifulSoup(html.read(), "html.parser")
    teamLinks,teamNames = getTeamsLinksAndNames(soup)
    teamMaleAthleteLinks, teamMaleAthleteNames = getTeamsAthleteLinksAndNames(teamLinks)
    womensLinks = []
    for each in teamLinks:
        womensLinks.append(each.replace('_m_','_f_'))
    teamFemaleAthleteLinks, teamFemaleAthleteNames = getTeamsAthleteLinksAndNames(womensLinks)
    teamAthleteLinks,teamAthleteNames=[],[]
    for index,each in enumerate(teamMaleAthleteLinks):
        teamAthleteLinks.append(each+teamFemaleAthleteLinks[index])
        teamAthleteNames.append(teamMaleAthleteNames[index]+teamFemaleAthleteNames[index])
    for teamIndex, eachTeamLink in enumerate(teamLinks):
        html = urlopen(eachTeamLink)
        soup=BeautifulSoup(html.read(), "html.parser")
        lastXMeets = getTeamsLastXMeets(soup)
        initalDictionary = []
        print(f"Current team is {teamNames[teamIndex]} {teamIndex + 1}/{len(teamNames)}")
        for athleteIndex,eachAthleteLink in enumerate(teamAthleteLinks[teamIndex]):
            #get their meet reuslt and check if pr recent
            percent = (athleteIndex + 1) / len(teamAthleteLinks[teamIndex]) * 100
            print(f"Progress: {percent:.2f}%", end="\r")
            html=urlopen(eachAthleteLink)
            soup=BeautifulSoup(html.read(), "html.parser")
            athleteRecentMeetURLs, athletesRecentMeets= getAthletesLastXMeets(soup)
            ##**COMPARE THE MEETS IF IT IS A SCHOOLS MOST RECENT CHECK FOR PRS IF NOT SKIP**##
            for meetIndex,eachMeet in enumerate(athleteRecentMeetURLs):
                if (lastXMeets[meetIndex] in eachMeet):
                    inputDate = athletesRecentMeets[meetIndex].find('span').text.strip()
                    #Special case for dates like April 13-14, 2021
                    if '-' in inputDate:
                        split = inputDate.split('-')
                        split2 = split[1].split(',')
                        inputDate = split[0] +','+split2[1]
                    format="%b %d, %Y"
                    meetDate = datetime.strptime(inputDate,format).date()
                    meetName = athletesRecentMeets[meetIndex].find('thead').find('a').text.strip()
                    allPRsAtPRMeet = athletesRecentMeets[meetIndex].findAll('tr', class_='highlight')
                    for eachPRatPRMeet in allPRsAtPRMeet:
                        eventName = eachPRatPRMeet.find('td').text.strip()
                        pr = eachPRatPRMeet.find('a').text.strip()
                        initalDictionary.append((teamAthleteNames[teamIndex][athleteIndex],meetName,eventName,pr,meetDate))
        prepForJSON=[]
        sortedDictByDate = {k: list(g) for k, g in groupby(sorted(initalDictionary, key=lambda x: x[4], reverse=True), key=lambda x: x[4])}
        for eachDate,meetsAtDate in sortedDictByDate.items():
            sortedByMeet = {k: list(g) for k, g in groupby(sorted(meetsAtDate, key=lambda x: x[1]), key=lambda x: x[1])}
            for eachMeet,prs in sortedByMeet.items():
                listOfPRS = []
                uniqueNames=[]
                uniqueNameCount=0
                for eachPR in prs:
                    if (eachPR[0] not in uniqueNames):
                        uniqueNames.append(eachPR[0])
                        uniqueNameCount+=1;
                    listOfPRS.append({"athletename":eachPR[0],"eventname":eachPR[2],"pr":eachPR[3]})
                jsonMeetOBJ = {"meetname":eachMeet,
                            "meetdate":prs[0][4].strftime(format),
                            "numberofprs":len(prs),
                            "uniqueprs":uniqueNameCount,
                            "prsatmeet":listOfPRS}
                prepForJSON.append(jsonMeetOBJ)
        fileName = BASE_DIR / f'{slugify(teamNames[teamIndex])}_recentrPRs.json'
        f = open(fileName, "w")
        f.write(json.dumps(prepForJSON, indent=4))
        f.close()
