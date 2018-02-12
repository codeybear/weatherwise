from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.http import Http404

from schedule.models import Activity, ActivityService

def index(request, schedule_id):
    activityService = ActivityService
    activities = activityService.GetByScheduleId(schedule_id)    
    
    template = loader.get_template('activity/index.html')
    context = { 'activities' : activities, 'viewtype' : 'index', 'ScheduleId' : schedule_id }
    return HttpResponse(template.render(context, request))

def detail(request, activity_id):
    activityService = ActivityService
    activity = Activity()

    if activity_id != 0:
        activity = ActivityService.GetById()

    template = loader.get_template('activity/index.html')    

    context = { 'activity' : activity, 'viewtype' : 'detail' }
    return HttpResponse(template.render(context, request))
    
def update(request, activity_id):
    activityService = ActivityService
    activity = Activity()

    activity.Id = activity_id
    activity.Name = request.POST['name']
    activity.Duration = request.POST['duration']

    if activity.Id == 0:
        activityService.Add(activity)
    else:
        activityService.Update(activity)

    return HttpResponseRedirect(f"/schedule/activity/{activity.ScheduleId}/index")