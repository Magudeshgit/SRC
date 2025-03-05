from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import *


class deptfilter(SimpleListFilter):
    title = "Department Wise"
    parameter_name = "Pseudo Department"
    
    def lookups(self, request, model_admin):
        departments = [('bad', 'bad'),
                       ('bsc', 'bsc'),
                       ('bcs', 'bcs'),
                       ('bam', 'bam'),
                       ('bit', 'bit'),
                       ('bee', 'bee'),
                       ('bev', 'bev'),
                       ('bec', 'bec'),
                       ('bau', 'bau'),
                       ('bce', 'bce'),
                       ('bme', 'bme'),
                       ]
        
        return departments

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(roll__icontains = self.value())
    
    
class yearfilter(SimpleListFilter):
    title = "Year Wise"
    parameter_name = "Year Wise"
    
    def lookups(self, request, model_admin):
        yos = [
                ('24', 'First Year'),
                ('23', 'Second Year'),
                ('22', 'Third Year'),
                ('21', 'Final Year'),
                ]
        return yos
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(roll__icontains = self.value())

class submissionModel(admin.ModelAdmin):
    list_filter = ['macroevent', 'microevent', 'registrar__department', 'registrar__yos']
    
class teammemberModel(admin.ModelAdmin):
    list_filter = ['macroevent', 'event', 'attendance', 'reviewed', deptfilter, yearfilter]
    
admin.site.register(submission, submissionModel)
admin.site.register(teammember, teammemberModel)
admin.site.register([macroevent, microevent, review, review_feeback, review_question])