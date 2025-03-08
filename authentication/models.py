from django.db import models
from django.contrib.auth.models import AbstractUser

class stream(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class department(models.Model):
    stream_of = models.ForeignKey(stream, on_delete=models.SET_NULL, null=True, blank=True)
    dept_name = models.CharField(max_length=50)
    dept_pseudo = models.CharField(max_length=10)
    association_name = models.CharField(max_length=100)
    coordinatorname = models.CharField(max_length=150)
    contact = models.CharField(max_length=22)
    
    def __str__(self):
        return self.dept_name
    
class User(AbstractUser):
    first_name = None
    last_name = None
    full_name = models.CharField(max_length=100)
    department = models.ForeignKey(department, on_delete=models.SET_NULL, null=True)
    yos = models.CharField(choices=(
        ("FIRST", "First Year"),
        ("SECOND", "Second Year"),
        ("THIRD", "Third Year"),
        ("FINAL", "Final Year")
    ), max_length=10)
    contact = models.CharField(max_length=12)
    collegemail = models.EmailField()
    
    # EMAIL_FIELD = "personalmail"
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return self.username