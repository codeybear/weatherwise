from django.http import HttpResponse
from django.template import loader
from django.http import Http404

class Schedule:
    Id = 0    
    Name = ""
    StartDate = ""

def index(request):
    schedule = Schedule
    schedule.Id = 1
    schedule.Name = "Test schedule 2"
    schedule.StartDate = "1/11/2017"

    template = loader.get_template('schedule/index.html')
    context = { 'schedule' : schedule }
    return HttpResponse(template.render(context, request))

def detail(request, schedule_id):
    if schedule_id == 9:
        raise Http404('Schedule does not exist')

    schedule = Schedule
    schedule.Id = schedule_id
    schedule.Name = "Test schedule 3"
    schedule.StartDate = "1/11/2017"

    template = loader.get_template('schedule/detail.html')
    context = { 'schedule' : schedule }
    return HttpResponse(template.render(context, request))

def update(request, schedule_id):
    return HttpResponse(f"Will done on saving {schedule_id}!")