from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.http import Http404

from schedule.models import Activity, ActivityService, Location, LocationService

def index(request, schedule_id):
    activityService = ActivityService
    activities = activityService.GetByScheduleId(schedule_id)    
    
    template = loader.get_template('activity/index.html')
    context = { 'activities' : activities, 'viewtype' : 'index', 'scheduleId' : schedule_id }
    return HttpResponse(template.render(context, request))

def detail(request, activity_id):
    scheduleId = request.GET["schedule_id"]
    activityService = ActivityService
    activity = Activity()
    locationService = LocationService

    if activity_id != 0:
        activity = ActivityService.GetById(activity_id)
    else:
        activity.Id = 0

    locations = locationService.GetByScheduleId(scheduleId)
    activityTypes = activityService.GetActivityTypes()
    template = loader.get_template('activity/detail.html')    

    context = { 'activity' : activity, 'locations': locations, 'activitytypes' : activityTypes , 'viewtype' : 'detail', 'scheduleId' : scheduleId }
    return HttpResponse(template.render(context, request))
    
def update(request, activity_id):
    activityService = ActivityService
    activity = Activity()

    activity.Id = activity_id
    activity.Name = request.POST['name']
    activity.Duration = request.POST['duration']
    activity.ScheduleId = request.POST['schedule_id']
    activity.LocationId = request.POST['location']
    activity.ActivityTypeId = request.POST['activity-type']

    if activity.Id == 0:
        activityService.Add(activity)
    else:
        activityService.Update(activity)

    return HttpResponseRedirect(f"/schedule/activity/{activity.ScheduleId}")