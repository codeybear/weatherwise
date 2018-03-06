from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader

from schedule.models import Weather

import time

def index(request, schedule_id):
    weather = Weather(schedule_id)

    start_time = time.time()
    
    activities = weather.CalcScheduleDuration()
    
    print("My program took" + str(time.time() - start_time) + "to run")
    
    template = loader.get_template('report/index.html')
    context = { 'activities' : activities }
    return HttpResponse(template.render(context, request))