from django.core.management.base import BaseCommand
from prs.models import *
import json
import fetchDataToAddOrUpdateDB

class Command(BaseCommand):
    help = 'Update, insert, or delete relevant data in the database'

    def handle(self, *args, **options):
        #call relevant functions from fetchData(etc).py
        json_data=fetchDataToAddOrUpdateDB.getTheDataReturnJson()

        colleges = json_data.get('Colleges', [])
        total_colleges = len(colleges)

        for college_index, college_data in enumerate(colleges, 1):
            college_name = college_data.get('CollegeName')
            college_link = college_data.get('CollegeLink')
            athletes = college_data.get('Athletes')
            college, _ = College.objects.get_or_create(college_name=college_name,college_link = college_link)
            
            total_athletes = len(athletes)
            self.stdout.write(f"{college_name} {college_index}/{total_colleges}")

            for athlete_index, athlete_data in enumerate(athletes, 1):
                athlete_name = athlete_data.get('Name')
                athlete_link = athlete_data.get('AthletesLink')
                prs = athlete_data.get('PRS')

                athlete, _ = Athlete.objects.get_or_create(athlete_name=athlete_name,
                                                                           athlete_link = athlete_link,
                                                                           college=college)

                progress = athlete_index / total_athletes * 100
                self.stdout.write(f"Progress: {progress:.2f}%  ", ending='\r')

                for pr_data in prs:
                    event_name = pr_data.get('EventName')
                    event, _ = Event.objects.get_or_create(event_name=event_name)

                    pr = pr_data.get('EventMark')
                    pr_link = pr_data.get('PRLink')

                    Personal_Record.objects.update_or_create(
                        athlete=athlete,
                        event=event,
                        pr = pr,
                        pr_link = pr_link
                    )

            self.stdout.write('\n')  # Move to the next line after processing all athletes of a college


"""
Json data will be like this
"Colleges":[
    {
        "CollegeName":name
        "CollegeLink":link
        "Athletes":[
            {
                "Name":name
                "AthletesLink":link
                "PRS":[
                    {
                        "EventName":name
                        "EventMark" :mark
                        "PRLink" :prlink
                    }
                ]
            }
        ]
    }
]
"""
