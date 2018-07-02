from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader

from schedule.models import Weather, ActivityService, Activity, ReportType

import time
import datetime

def index(request, schedule_id):
    reportType = int(request.GET["reporttype"])
    weather = Weather(schedule_id)
    activities = []
    originalLabel = "Planned dur"
    newLabel = "Actual dur"

    if reportType == 1:
        result = weather.CalcScheduleDuration(calcType = ReportType.NORMAL)
    if reportType == 2:
        result = weather.CalcScheduleDuration(calcType = ReportType.WEATHER_AWARE)
    if reportType == 4:
        result = weather.CalcScheduleDuration(calcType = ReportType.REVERSE)
        originalLabel, newLabel = newLabel, originalLabel
    
    activities = result[0]
    duration = result[1]
    template = loader.get_template('report/index.html')
    context = { 'activities' : activities, 'dependencies' : weather.dependencyList, 'scheduleId' : schedule_id, 
                'duration' : duration, 'reportType' : reportType, 'originalLabel' : originalLabel, 'newLabel' : newLabel }
    return HttpResponse(template.render(context, request))

def daysindex(request, schedule_id):
    weather = Weather(schedule_id)
    durationList, endDateList = weather.CalcDaysOfYear()

    template = loader.get_template('report/daysindex.html')
    context = { 'durationList' : durationList, 'endDateList' : endDateList ,'scheduleId' : schedule_id }
    return HttpResponse(template.render(context, request))

def stochasticindex(request, schedule_id):
    iterCount = int(request.GET.get('itercount', 1000))
    duration = int(request.GET.get('duration', 0))
    reportType = int(request.GET.get('type', 2))
    weather = Weather(schedule_id)
    durationList = []

    if reportType == 2:
        durationList = weather.CalcStochastic(iterCount, ReportType.WEATHER_AWARE)
    if reportType == 4:
        durationList = weather.CalcStochastic(iterCount, ReportType.REVERSE)

    template = loader.get_template('report/stochasticindex.html')
    context = { 'durationList' : durationList, 'scheduleId' : schedule_id, 'duration' : duration }
    return HttpResponse(template.render(context, request))