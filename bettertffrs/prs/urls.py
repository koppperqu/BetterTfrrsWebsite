from django.urls import path

from . import views

urlpatterns = [
    path('athlete/<int:athlete_id>', views.athlete, name='athlete'),
    path('event/<int:event_id>', views.event, name='event'),
]