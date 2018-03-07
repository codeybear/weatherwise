from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader

from schedule.models import Weather

import time
import datetime

def index(request, schedule_id):
    weather = Weather(schedule_id)

    start_time = time.time()
    today = datetime.now()

    for x in range(1,100000):
        today += datetime.timedelta(days=1)

    # for x in range(1,100):
    #     activities = weather.CalcScheduleDuration()
    print(today)
    print("Program took " + str(time.time() - start_time) + " to run")
    
    template = loader.get_template('report/index.html')
    context = { 'activities' : activities }
    return HttpResponse(template.render(context, request))