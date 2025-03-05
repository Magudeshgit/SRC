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
    timestamp = models.DateTimeField(auto_now_add=True)
    
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
    created_at = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)
    
    submission = models.ForeignKey(submission, on_delete=models.CASCADE)
    event = models.ForeignKey(microevent, on_delete=models.CASCADE)
    macroevent = models.ForeignKey(macroevent, on_delete=models.CASCADE)
    
    attendance = models.BooleanField(default=False)
    is_registrar = models.BooleanField(default=False)
    reviewed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
class review(models.Model):
    reviewer = models.CharField(max_length=20)
    total_marks = models.IntegerField()
    event = models.ForeignKey(microevent, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.event.eventname
    
class review_question(models.Model):
    question = models.TextField(max_length=250)
    max_marks = models.IntegerField()
    event = models.ForeignKey(microevent, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.question

class review_feeback(models.Model):
    review = models.ForeignKey(review, on_delete=models.CASCADE)
    review_question = models.ForeignKey(review_question, on_delete=models.CASCADE)
    mark = models.IntegerField()
    event = models.ForeignKey(microevent, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.review_question
    
    