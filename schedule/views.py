from django.http import HttpResponse
from django.template import loader
from django.http import Http404

from schedule.models import MyClass, Schedule, ScheduleService

#class Schedule:
#    Id = 0    
#    Name = ""
#    StartDate = ""

def index(request):
    schedule = Schedule
    schedule.Id = 1
    schedule.Name = "Test Schedule"
    schedule.StartDate = "1/11/2017"

    template = loader.get_template('schedule/index.html')
    context = { 'schedule' : schedule }
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
    schedule.Id = request.POST['Id']
    schedule.Name = request.POST['Name']
    schedule.StartDate = request.POST['StartDate']
    schedule.WorkingDay0 = request.POST['WorkingDay0']

    scheduleService = ScheduleService
    #scheduleService.update(schedule)

    #return HttpResponse(f"Well done on saving {schedule_id}!")
    return HttpResponseRedirect(reverse('schedule:index', args=(schedule.Name,)))