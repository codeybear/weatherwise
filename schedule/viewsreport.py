import enum
from django.conf import settings
from django.http import HttpResponse
from django.template import loader

from schedule.models import Weather, ReportType, ScheduleService


def index(request, schedule_id):
    fromSchedules = request.GET.get('fromschedules', False)
    reportType = int(request.GET["reporttype"])
    weather = Weather(schedule_id)
    statusDate = GetStatusDate(schedule_id)
    originalLabel = "Planned dur"
    newLabel = "Actual dur"

    if reportType == 2:
        activities, duration, _ = weather.CalcScheduleDuration(calcType=ReportType.WEATHER_AWARE)
        activities2, duration2, _ = weather.CalcScheduleDuration(calcType=ReportType.NORMAL)

        for idx, _ in enumerate(activities):
            activities2[idx].NewDuration = activities[idx].NewDuration

    if reportType == 4:
        # Get the weather aware durations as we want to work backwards from these predictions
        activities, duration, _ = weather.CalcScheduleDuration(calcType=ReportType.WEATHER_AWARE)

        for activity in activities:
            activity.Duration, activity.NewDuration = activity.NewDuration, activity.Duration

        for activity in weather.activityList:
            activity.Duration = activity.NewDuration

        # Get the planned activity durations from the weather aware durations
        activities2, duration2, _ = weather.CalcScheduleDuration(calcType=ReportType.REVERSE)

        originalLabel, newLabel = newLabel, originalLabel

    context = {'activities': activities, 'activities2': activities2, 'dependencies': weather.dependencyList,
               'scheduleId': schedule_id, 'duration': duration, 'duration2': duration2, 'reportType': reportType,
               'originalLabel': originalLabel, 'newLabel': newLabel, 'fromSchedules': fromSchedules,
               'statusDate': statusDate}

    template = loader.get_template('report/index.html')
    return HttpResponse(template.render(context, request))


def daysindex(request, schedule_id):
    weather = Weather(schedule_id)
    weather.schedule.StatusTypeId = 1
    durationList, endDateList = weather.CalcDaysOfYear()

    template = loader.get_template('report/daysindex.html')
    context = {'durationList': durationList, 'endDateList': endDateList, 'scheduleId': schedule_id}
    return HttpResponse(template.render(context, request))


def stochasticindex(request, schedule_id):
    duration = 0
    durationCDF = 0
    iterCount = int(request.GET.get('itercount', 1000))
    reportType = int(request.GET.get('type', 2))
    weather = Weather(schedule_id)
    durationList = []
    demoMode = settings.DEMO_MODE

    if reportType == 2:
        durationList = weather.CalcStochastic(iterCount, ReportType.WEATHER_AWARE)
    if reportType == 4:
        # This should be the weather aware point, even though it is unlikely to show
        _, duration, _ = CalcReverseReport(schedule_id)
        weather.schedule.StatusTypeId = 1
        durationList = weather.CalcStochastic(iterCount, ReportType.REVERSE, duration)

        # find the probability for the marked point
        itemCDF = [item for item in durationList if item[1] == duration]
        if len(itemCDF) > 0: durationCDF = itemCDF[0][0]

    template = loader.get_template('report/stochasticindex.html')
    context = {'durationList': durationList, 'scheduleId': schedule_id, 'startDate': weather.schedule.StartDate,
               'duration': duration, 'durationCDF': durationCDF, 'reportType': reportType, 'demoMode': demoMode}

    return HttpResponse(template.render(context, request))


def CalcReverseReport(scheduleId):
    """"This is to mark a point on the reverse report that shows where the weather aware
    duration appears"""
    # Get the weather aware durations and set these durations for the reverse report
    weather = Weather(scheduleId)
    weather.schedule.StatusTypeId = 1

    result = weather.CalcScheduleDuration(calcType=ReportType.WEATHER_AWARE)

    for idx, activity in enumerate(weather.activityList):
        weather.activityList[idx].Duration = result[0][idx].NewDuration

    # Get the planned durations from the weather aware durations
    result = weather.CalcScheduleDuration(calcType=ReportType.REVERSE)

    return result


def GetStatusDate(scheduleId):
    scheduleService = ScheduleService
    schedule = scheduleService.GetById(scheduleId)

    if schedule.StatusTypeId == 2:
        return schedule.StatusDateDisplay
    else:
        return ""
