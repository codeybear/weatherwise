from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.http import Http404

from schedule.models import MyClass, Schedule, ScheduleService

def index(request):
    template = loader.get_template('location/index.html')
    context = { 'schedules' : '' }
    return HttpResponse(template.render(context, request))