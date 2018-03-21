from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader

from schedule.models import Weather, ActivityService, Activity

import time
import datetime

def index(request, schedule_id):
    weather = Weather(schedule_id)
    activities = weather.CalcScheduleDuration()
    
    template = loader.get_template('report/index.html')
    context = { 'activities' : activities, 'dependencies' : weather.dependencyList }
    return HttpResponse(template.render(context, request))

# activityService = ActivityService
# activities = activityService.GetByScheduleId(schedule_id)

# start_time = time.time()
# today = datetime.datetime.now()

# for x in range(1,1000000):
#     today += datetime.timedelta(days=1)

# for x in range(1,100):
#     activities = weather.CalcScheduleDuration()
# print(today)
# print("Program took " + str(time.time() - start_time) + " to run")