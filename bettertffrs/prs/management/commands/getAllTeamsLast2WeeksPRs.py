from django.core.management.base import BaseCommand
from prs.models import *
import json

class Command(BaseCommand):
    help = 'Gets all teams last 2 weeks prs and puts them in individual files'

    def handle(self, *args, **options):
        #call the function that runs the script to get all teams prs in alst 2 weeks