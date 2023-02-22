from django.urls import path

from . import views

urlpatterns = [
    path('athletes/',views.athletes, name='athletes'),
    path('athlete/<int:athlete_id>', views.athlete, name='athlete'),
    path('events/<int:id>', views.event, name='event'),
    path('events/', views.events, name='events'),
]