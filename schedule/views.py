from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.http import Http404

import time
from schedule.models import Schedule, ScheduleService

def index(request):
    scheduleService = ScheduleService
    schedules = scheduleService.GetAll()    

    template = loader.get_template('schedule/index.html')
    context = { 'schedules' : schedules }
    return HttpResponse(template.render(context, request))

def detail(request, schedule_id):
    if schedule_id == 9:
        raise Http404('Schedule does not exist')

    scheduleService = ScheduleService
    schedule = Schedule
    
    if schedule_id != 0:
        schedule = scheduleService.GetById(schedule_id)

    template = loader.get_template('schedule/detail.html')
    context = { 'schedule' : schedule }
    return HttpResponse(template.render(context, request))

def update(request, schedule_id):
    schedule = Schedule
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

    scheduleService = ScheduleService

    if schedule_id != 0:
        scheduleService.Update(schedule)
    else:
        scheduleService.Add(schedule)

    return HttpResponseRedirect('/schedule')
    #return HttpResponseRedirect(reverse('schedule:index'))
    #return HttpResponseRedirect(reverse('schedule:detail', args=(schedule.Id)))

def IsChecked(dict, item):
    if dict.get(item, 0) == '':
        return True
    else:
        return False