from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.conf import settings

from schedule.models import Weather, ActivityService, Activity, ReportType, ScheduleService

import time
import datetime

def index(request, schedule_id):
    fromSchedules = request.GET.get('fromschedules', False)    
    reportType = int(request.GET["reporttype"])
    weather = Weather(schedule_id)
    statusDate = GetStatusDate(schedule_id)
    originalLabel = "Planned dur"
    newLabel = "Actual dur"

    if reportType == 1:
        result = weather.CalcScheduleDuration(calcType = ReportType.NORMAL)
    if reportType == 2:
        result = weather.CalcScheduleDuration(calcType = ReportType.WEATHER_AWARE)
        result2 = weather.CalcScheduleDuration(calcType = ReportType.NORMAL)
    if reportType == 4:
        # Get the weather aware durations and set these durations for the reverse report
        result = weather.CalcScheduleDuration(calcType = ReportType.WEATHER_AWARE)
        
        for idx, activity in enumerate(weather.activityList):
            weather.activityList[idx].Duration = result[0][idx].NewDuration

        # Get the planned durations from the weather aware durations
        result = weather.CalcScheduleDuration(calcType = ReportType.REVERSE)

        # Calculate the start and end dates for these activities using the normal report
        for idx, activity in enumerate(weather.activityList):
            weather.activityList[idx].Duration = result[0][idx].NewDuration     
           
        result2 = weather.CalcScheduleDuration(calcType = ReportType.NORMAL)

        originalLabel, newLabel = newLabel, originalLabel
    
    activities = result[0]
    duration = result[1]
    activities2 = result2[0]
    duration2 = result2[1]

    for idx, activity in enumerate(activities):
        if reportType == 4:
            activities2[idx].Duration = activities[idx].Duration
        if reportType == 2:
            activities2[idx].NewDuration = activities[idx].NewDuration

    template = loader.get_template('report/index.html')

    context = { 'activities' : activities, 'activities2' : activities2 , 'dependencies' : weather.dependencyList, 'scheduleId' : schedule_id, 
                'duration' : duration, 'duration2' : duration2 ,'reportType' : reportType, 'originalLabel' : originalLabel, 'newLabel' : newLabel, 
                'fromSchedules' : fromSchedules, 'statusDate' : statusDate  }
    return HttpResponse(template.render(context, request))

def daysindex(request, schedule_id):
    weather = Weather(schedule_id)
    weather.schedule.StatusTypeId = 1
    durationList, endDateList = weather.CalcDaysOfYear()

    template = loader.get_template('report/daysindex.html')
    context = { 'durationList' : durationList, 'endDateList' : endDateList ,'scheduleId' : schedule_id }
    return HttpResponse(template.render(context, request))

def stochasticindex(request, schedule_id):
    duration = 0
    durationCDF = 0
    iterCount = int(request.GET.get('itercount', 1000))
    reportType = int(request.GET.get('type', 2))
    weather = Weather(schedule_id)
    durationList = []
    demoMode = settings.DEMO_MODE

    scheduleService = ScheduleService()
    schedule = scheduleService.GetById(schedule_id)

    if reportType == 2:
        durationList = weather.CalcStochastic(iterCount, ReportType.WEATHER_AWARE)
    if reportType == 4:
        # Get the weather aware durations and set these durations for the reverse report
        result = CalcReverseReport(schedule_id)        
        duration = result[1]
        durationList = weather.CalcStochastic(iterCount, ReportType.REVERSE, duration)
        itemCDF = [item for item in durationList if item[1] == duration]

        if len(itemCDF) > 0:
            durationCDF = itemCDF[0][0]

    template = loader.get_template('report/stochasticindex.html')
    context = { 'durationList' : durationList, 'scheduleId' : schedule_id, 'startDate' : schedule.StartDate , 'duration' : duration, 
                'durationCDF' : durationCDF, 'reportType' : reportType, 'demoMode' : demoMode}
    return HttpResponse(template.render(context, request))

def CalcReverseReport(scheduleId):
    # Get the weather aware durations and set these durations for the reverse report
    weather = Weather(scheduleId)
    weather.schedule.StatusTypeId = 1

    result = weather.CalcScheduleDuration(calcType = ReportType.WEATHER_AWARE)

    for idx, activity in enumerate(weather.activityList):
        weather.activityList[idx].Duration = result[0][idx].NewDuration

    # Get the planned durations from the weather aware durations
    result = weather.CalcScheduleDuration(calcType = ReportType.REVERSE)

    # Calculate the start and end dates for these activities using the normal report
    for idx, activity in enumerate(weather.activityList):
        weather.activityList[idx].Duration = result[0][idx].NewDuration     

    result = weather.CalcScheduleDuration(calcType = ReportType.NORMAL)        
    return result

def GetStatusDate(scheduleId):
    scheduleService = ScheduleService
    schedule = scheduleService.GetById(scheduleId)

    if schedule.StatusTypeId == 2:
        return schedule.StatusDateDisplay
    else:
        return ""

