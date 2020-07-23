import time

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from schedule.models import Schedule, ScheduleService, ActivityService, LocationService


def index(request):
    demoMode = settings.DEMO_MODE
    scheduleService = ScheduleService
    schedules = scheduleService.GetAll()

    template = loader.get_template('schedule/index.html')
    context = {'schedules': schedules, 'demoMode': demoMode}
    return HttpResponse(template.render(context, request))


def detail(request, schedule_id):
    scheduleService = ScheduleService
    schedule = Schedule
    statusTypes = scheduleService.GetStatusTypes()
    demoMode = settings.DEMO_MODE

    if schedule_id != 0:
        schedule = scheduleService.GetById(schedule_id)

    template = loader.get_template('schedule/detail.html')
    context = {'schedule': schedule, 'scheduleId': schedule_id, 'demoMode': demoMode, 'statusTypes': statusTypes}
    return HttpResponse(template.render(context, request))


def update(request, schedule_id):
    schedule = Schedule()
    schedule.Id = request.POST['id']
    schedule.Name = request.POST['name']
    schedule.StartDateDisplay = request.POST['startdate']
    schedule.StartDate = time.strptime(schedule.StartDateDisplay, "%d/%m/%Y")
    schedule.StatusTypeId = request.POST['statustype']
    schedule.StatusDateDisplay = request.POST.get('statusdate', '')
    schedule.StatusDate = time.strptime(schedule.StatusDateDisplay,
                                        "%d/%m/%Y") if schedule.StatusDateDisplay != '' else None
    # TODO move this into the model
    schedule = CheckWorkingDays(request, schedule)
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
    context = {'activities': len(activities), 'scheduleId': schedule_id, 'locations': len(locations)}
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


def CheckWorkingDays(request, schedule):
    for item in range(0, 6):
        schedule.__dict__["WorkingDay" + str(item)] =  IsChecked(request.POST, 'workingday' + str(item))

    return schedule
