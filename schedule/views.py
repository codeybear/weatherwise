from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.http import Http404

from schedule.models import MyClass, Schedule, ScheduleService

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
    schedule = scheduleService.GetById(schedule_id)

    template = loader.get_template('schedule/detail.html')
    context = { 'schedule' : schedule }
    return HttpResponse(template.render(context, request))

def update(request, schedule_id):
    schedule = Schedule
    schedule.Id = request.POST['id']
    schedule.Name = request.POST['name']
    schedule.StartDate = request.POST['startdate']
    #schedule.WorkingDay0 = request.POST['workingday0']

    scheduleService = ScheduleService
    scheduleService.Update(schedule)

    #return HttpResponse(f"Well done on saving {schedule_id}!")
    return HttpResponseRedirect(reverse('schedule:detail', args=(schedule.Id)))