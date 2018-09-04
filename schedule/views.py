from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.http import Http404
from django.conf import settings

import time
from schedule.models import Schedule, ScheduleService, ActivityService, LocationService

def index(request):
    demoMode = settings.DEMO_MODE
    scheduleService = ScheduleService
    schedules = scheduleService.GetAll()
    
    template = loader.get_template('schedule/index.html')
    context = { 'schedules' : schedules, 'demoMode' : demoMode }
    return HttpResponse(template.render(context, request))

def detail(request, schedule_id):
    scheduleService = ScheduleService
    schedule = Schedule
    demoMode = settings.DEMO_MODE
    
    if schedule_id != 0:
        schedule = scheduleService.GetById(schedule_id)
    else:
        schedule.Id == 0

    template = loader.get_template('schedule/detail.html')
    context = { 'schedule' : schedule, 'scheduleId' : schedule_id, 'demoMode' : demoMode  }
    return HttpResponse(template.render(context, request))

def update(request, schedule_id):
    schedule = Schedule()
    schedule.Id = request.POST['id']
    schedule.Name = request.POST['name']
    schedule.StartDateDisplay = request.POST['startdate']
    schedule.StartDate = time.strptime(schedule.StartDateDisplay, "%d/%m/%Y")

    schedule.WorkingDay0 = IsChecked(request.POST, 'workingday0')
    schedule.WorkingDay1 = IsChecked(request.POST, 'workingday1')
    schedule.WorkingDay2 = IsChecked(request.POST, 'workingday2')
    schedule.WorkingDay3 = IsChecked(request.POST, 'workingday3')
    schedule.WorkingDay4 = IsChecked(request.POST, 'workingday4')
    schedule.WorkingDay5 = IsChecked(request.POST, 'workingday5')
    schedule.WorkingDay6 = IsChecked(request.POST, 'workingday6')

    if schedule.WorkingDay0 == False and schedule.WorkingDay1 == False and schedule.WorkingDay2 == False and schedule.WorkingDay3 == False and schedule.WorkingDay4 == False and schedule.WorkingDay5 == False and schedule.WorkingDay6 == False:
        schedule.WorkingDay0 = True
        schedule.WorkingDay1 = True
        schedule.WorkingDay2 = True
        schedule.WorkingDay3 = True
        schedule.WorkingDay4 = True

    scheduleService = ScheduleService

    if schedule_id != 0:
        scheduleService.Update(schedule)
    else:
        scheduleService.Add(schedule)

    return HttpResponseRedirect('/schedule')

def deleteindex(request, schedule_id):
    activityService = ActivityService
    locationService = LocationService
    # Need to check to see if there are dependencies related to this activity
    activities = activityService.GetByScheduleId(schedule_id)
    locations = locationService.GetByScheduleId(schedule_id)

    template = loader.get_template('schedule/delete.html')
    context = { 'activities' : len(activities), 'scheduleId' : schedule_id, 'locations' : len(locations)}
    return HttpResponse(template.render(context, request))

def delete(request, schedule_id):
    scheduleService = ScheduleService
    scheduleService.Delete(schedule_id)
    return HttpResponseRedirect("/")
    
def IsChecked(dict, item):
    if dict.get(item, 0) == '':
        return True
    else:
        return False