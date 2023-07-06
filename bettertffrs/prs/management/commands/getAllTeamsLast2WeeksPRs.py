from django.core.management.base import BaseCommand
import getAllTeamsLast2WeeksPRs

class Command(BaseCommand):
    help = 'Gets all teams last 2 weeks prs and puts them in individual files'

    def handle(self, *args, **options):
        getAllTeamsLast2WeeksPRs.getAllTeamsLast2WeeksPrsPutInJSONFormat()