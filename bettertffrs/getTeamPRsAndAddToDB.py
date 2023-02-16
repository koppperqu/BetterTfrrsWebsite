from urllib.request import urlopen
from bs4 import BeautifulSoup
import sqlite3
mensTrackURL = 'https://www.tfrrs.org/teams/tf/WI_college_m_Wis_Stevens_Point.html'
html = urlopen(mensTrackURL)
soup=BeautifulSoup(html.read(), "html.parser")
womensTrackURL = 'https://www.tfrrs.org'+soup.find('a',string='Women\'s Track & Field')['href']

#This functon takes the input ur and finds the roster section on the page then grabs all the names and tfrrs links and returns them as a dictionary as key value pairs name is the key
def getAthletesNamesAndTfrrsLinks(url):
    html = urlopen(url)
    soup=BeautifulSoup(html.read(), "html.parser")
    athleteLinks = soup.find('h3',string='ROSTER').find_parent().find('tbody').findAll('a')
    names=[]
    tfrrsLink=[]
    for eachLink in athleteLinks:
        nameParts=eachLink.getText().split(', ')
        names.append(nameParts[1]+' '+nameParts[0])
        tfrrsLink.append('https://www.tfrrs.org'+eachLink['href'])
    return(names,tfrrsLink)

def getEventsandPRSandAddToDB(names,tfrrsLinks):
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    for nameIndex,eachName in enumerate(names):
        res = cur.execute("select count(*) from prs_athlete where athlete_name = ?",(eachName,))
        count = res.fetchone()[0]
        if(count==0):
            cur.execute("insert into prs_athlete (athlete_name,tffrs_link_for_athlete) values(?,?)",(eachName,tfrrsLinks[nameIndex]))
            con.commit()
    for tfrrLinkindex,eachLink in enumerate(tfrrsLinks):#goes through each persons tfrrs page
        print (eachLink)
        html = urlopen(eachLink)
        soup=BeautifulSoup(html.read(), "html.parser")
        bests=soup.find('table',class_='table bests')#grabs the personal bests table
        bestsTD=bests.findAll('td')
        events=[]
        marks=[]
        athleteID = cur.execute("select athlete_id from prs_athlete where athlete_name = ?",(names[tfrrLinkindex],)).fetchone()[0]
        for index,each in enumerate(bestsTD):
            if index%2==0:
                events.append(each.getText().strip())
            else:
                marks.append(each.getText().strip())
        for eventIndex, eachEvent in enumerate(events):
            if eachEvent=="":
                break
            res = cur.execute("select count(*) from prs_event where event_name = ?",(eachEvent,))
            count = res.fetchone()[0]
            if(count==0):
                cur.execute("insert into prs_event (event_name) values(?)",(eachEvent,))
                con.commit()
            eventID = cur.execute("select event_id from prs_event where event_name = ?",(eachEvent,)).fetchone()[0]
            res = cur.execute("select count(*) from prs_personal_record where event_id = ? and athlete_id = ?",(eventID,athleteID))
            count = res.fetchone()[0]
            if(count==0):
                cur.execute("insert into prs_personal_record (athlete_id,event_id,pr) values(?,?,?)",(athleteID,eventID,marks[eventIndex]))
                con.commit()
            else:
                prID = "select pr_id from prs_personal_record where event_id = ? and athlete_id = ?",(eventID,athleteID)
                cur.execute("update prs_personal_record set pr = ? where pr_id = ?",(marks[eventIndex],prID,))
                con.commit()
    con.close()

men,menTfrrsLink = getAthletesNamesAndTfrrsLinks(mensTrackURL)
women,womenTfrrsLink = getAthletesNamesAndTfrrsLinks(womensTrackURL)
names = men+women
tfrrsLinks = menTfrrsLink + womenTfrrsLink
getEventsandPRSandAddToDB(names,tfrrsLinks)