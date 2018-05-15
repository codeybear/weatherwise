from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader

from schedule.models import Weather, ActivityService, Activity

import time
import datetime

def index(request, schedule_id):
    reportType = int(request.GET["reporttype"])
    weather = Weather(schedule_id)
    activities = []

    # TODO: add the additional reports here
    if reportType == 2:
        result = weather.CalcScheduleDuration()
        activities = result[0]
    
    template = loader.get_template('report/index.html')
    context = { 'activities' : activities, 'dependencies' : weather.dependencyList, 'scheduleId' : schedule_id }
    return HttpResponse(template.render(context, request))

def daysindex(request, schedule_id):
    weather = Weather(schedule_id)
    durationList, endDateList = weather.CalcDaysOfYear()

    template = loader.get_template('report/daysindex.html')
    context = { 'durationList' : durationList, 'endDateList' : endDateList ,'scheduleId' : schedule_id }
    return HttpResponse(template.render(context, request))