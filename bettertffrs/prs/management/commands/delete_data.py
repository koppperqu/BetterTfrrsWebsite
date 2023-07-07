from django.core.management.base import BaseCommand
from prs.models import *

class Command(BaseCommand):
    help = 'Delete all data in the Athlete model'

    def handle(self, *args, **options):
        Athlete.objects.all().delete()
        Personal_Record.objects.all().delete()
        Event.objects.all().delete()
        College.objects.all().delete()
