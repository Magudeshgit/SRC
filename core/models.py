from django.db import models
from authentication.models import User, department

class macroevent(models.Model):
    eventname = models.CharField(max_length=100)
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    is_banner = models.BooleanField()
    short_description = models.TextField(verbose_name="Short Description(max: 150 char)")
    long_description = models.TextField(verbose_name="Detailed Description")
    
    def __str__(self):
        return self.eventname

# might need to create table for stream and yos
class microevent(models.Model):
    micro_of = models.ForeignKey(macroevent, on_delete=models.CASCADE)
    eventname = models.CharField(max_length=100)
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    poster = models.FileField(upload_to='posters')
    
    short_description = models.TextField(verbose_name="Short Description(max: 150 char/card)")
    long_description = models.TextField(verbose_name="Detailed Description")
    round_details = models.TextField(verbose_name="Round details(Point wise desc. delimiter:\\n)")
    jury_details = models.TextField()
    event_venue = models.TextField(max_length=100)
    
    maximum_participation = models.IntegerField(verbose_name="Maximum Individuals")
    is_team_event = models.BooleanField()
    min_team_size = models.IntegerField()
    max_team_size = models.IntegerField()
    
    registration_closed = models.BooleanField()
    department = models.ForeignKey(department, on_delete=models.SET_NULL, null=True)
    student_coordinator = models.TextField()
    
    def __str__(self):
        return self.eventname

class submission(models.Model):
    macroevent = models.ForeignKey(macroevent, on_delete=models.CASCADE)
    microevent = models.ForeignKey(microevent, on_delete=models.CASCADE)
    
    teamname = models.CharField(max_length=50, null=True)
    registrar = models.ForeignKey(User, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.microevent.eventname

class teammember(models.Model):
    teamname = models.CharField(max_length=50, null=True)
    
    roll = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    contact = models.CharField(max_length=20)
    
    submission = models.ForeignKey(submission, on_delete=models.CASCADE)
    event = models.ForeignKey(microevent, on_delete=models.CASCADE)
    macroevent = models.ForeignKey(macroevent, on_delete=models.CASCADE)
    
    attendance = models.BooleanField()
    is_registrar = models.BooleanField()
    
    def __str__(self):
        return self.name