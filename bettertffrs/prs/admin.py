from django.contrib import admin

# Register your models here.

from .models import Athlete
admin.site.register(Athlete)
from .models import Event
admin.site.register(Event)
from .models import Personal_Record
admin.site.register(Personal_Record)