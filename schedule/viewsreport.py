from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader

from schedule.models import Weather, ActivityService, Activity

import time
import datetime

def index(request, schedule_id):
    weather = Weather(schedule_id)
    result = weather.CalcScheduleDuration()
    activities = result[0]
    
    template = loader.get_template('report/index.html')
    context = { 'activities' : activities, 'dependencies' : weather.dependencyList }
    return HttpResponse(template.render(context, request))

def daysindex(request, schedule_id):
    weather = Weather(schedule_id)
    durationList = weather.CalcDaysOfYear()

    template = loader.get_template('report/daysindex.html')
    context = { 'durationList' : durationList }
    return HttpResponse(template.render(context, request))
    