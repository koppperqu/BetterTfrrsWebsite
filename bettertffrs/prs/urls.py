from django.urls import path

from . import views

urlpatterns = [
    path('<slug:college_slug>/athletes/',views.athletes, name='athletes'),
    path('<slug:college_slug>/athlete/<int:athlete_id>/', views.athlete, name='athlete'),
    path('<slug:college_slug>/<slug:event_slug>/<int:id>/', views.event, name='event'),
    path('<slug:college_slug>/events/', views.events, name='events'),
    path('<slug:college_slug>/', views.college, name='college'),
]