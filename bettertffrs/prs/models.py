from django.db import models

# Create your models here.
class Athlete(models.Model):
    athlete_id = models.AutoField(primary_key=True)
    athlete_name = models.CharField(max_length=50)
    tffrs_link_for_athlete = models.CharField(max_length=100)
    athlete_gender_male = models.BooleanField()
    def __str__(self):
        return(self.athlete_name)

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=50)
    def __str__(self):
        return(self.event_name)

class Personal_Record(models.Model):
    pr_id = models.AutoField(primary_key=True)
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    distance = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank=True)
    time = models.TimeField(null = True, blank=True)
    def __str__(self):
        return(self.athlete.athlete_name + " " + self.event.event_name)
