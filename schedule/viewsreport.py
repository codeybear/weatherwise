from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader

from schedule.models import Weather

def index(request, schedule_id):
    weather = Weather(schedule_id)
    activities = weather.CalcScheduleDuration()
    
    template = loader.get_template('report/index.html')
    context = { 'activities' : activities }
    return HttpResponse(template.render(context, request))