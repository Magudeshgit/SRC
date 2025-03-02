from django.contrib import admin
from .models import *
admin.site.register([macroevent, microevent, submission, teammember])