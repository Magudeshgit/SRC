from django.db import models

class macroevent(models.Model):
    eventname = models.CharField(max_length=100)
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    
    short_description = models.TextField(verbose_name="Short Description(max: 150 char)")
    long_description = models.TextField(verbose_name="Detailed Description")
    
    def __str__(self):
        return self.eventname