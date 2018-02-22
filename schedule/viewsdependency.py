from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader

from schedule.models import Dependency, DependencyService

def index(request):
    scheduleService = ScheduleService
    schedules = scheduleService.GetAll()    

    template = loader.get_template('schedule/index.html')
    context = { 'schedules' : schedules }
    return HttpResponse(template.render(context, request))
