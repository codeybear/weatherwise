from django.http import HttpResponse
from django.template import loader

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
    schedule = Schedule
    schedule.Id = 1
    schedule.Name = "Test schedule 3"
    schedule.StartDate = "1/11/2017"

    template = loader.get_template('schedule/detail.html')
    context = { 'schedule' : schedule }
    return HttpResponse(template.render(context, request))