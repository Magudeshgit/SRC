from django.contrib import admin
from .models import *

class Useradmin(admin.ModelAdmin):
    list_display = ['full_name', 'username', 'department','yos']
    search_fields = ['full_name', 'username']
    list_filter = ['groups', 'yos', 'department']
admin.site.site_header = "Student Research Council"
admin.site.register([stream, department])
admin.site.register(User, Useradmin)