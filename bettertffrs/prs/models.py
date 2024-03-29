from django.db import models

# Create your models here.
class College(models.Model):
    college_id = models.AutoField(primary_key=True)
    college_name = models.CharField(max_length=50)
    college_link = models.CharField(max_length=100)
    def __str__(self):
        return self.college_name

class Athlete(models.Model):
    athlete_id = models.AutoField(primary_key=True)
    athlete_name = models.CharField(max_length=50)
    athlete_link = models.CharField(max_length=100)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
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
    pr = models.CharField(max_length=50)
    pr_link = models.CharField(max_length=100)
    def __str__(self):
        return(self.athlete.athlete_name + " " + self.event.event_name)
