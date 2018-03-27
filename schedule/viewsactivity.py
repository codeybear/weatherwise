from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.http import Http404, JsonResponse

from schedule.models import Activity, ActivityService, Location, LocationService, Dependency, DependencyService

def index(request, schedule_id):
    activityService = ActivityService
    activities = activityService.GetByScheduleId(schedule_id)    
    
    template = loader.get_template('activity/index.html')
    context = { 'activities' : activities, 'viewtype' : 'index', 'scheduleId' : schedule_id }
    return HttpResponse(template.render(context, request))

def detail(request, activity_id):
    scheduleId = request.GET["schedule_id"]
    activityService = ActivityService
    activities = activityService.GetByScheduleId(scheduleId)
    activity = Activity()
    locationService = LocationService

    if activity_id != 0:
        activity = ActivityService.GetById(activity_id)
    else:
        activity.Id = 0

    locations = locationService.GetByScheduleId(scheduleId)
    activityTypes = activityService.GetActivityTypes()

    template = loader.get_template('activity/detail.html')    
    context = { 'activity' : activity, 'locations': locations, 'activitytypes' : activityTypes , 'viewtype' : 'detail', 'scheduleId' : scheduleId, 'activities' : activities }
    return HttpResponse(template.render(context, request))
    
def update(request, activity_id):
    changePos = int(request.POST["selectPosition"])
    activityService = ActivityService
    activity = Activity()
    insertedId = 0

    activity.Id = activity_id
    activity.Name = request.POST['name']
    activity.Duration = request.POST['duration']
    activity.ScheduleId = request.POST['schedule_id']
    activity.LocationId = request.POST['location']
    activity.ActivityTypeId = request.POST['activity-type']

    if activity.Id == 0:
        insertedId = activityService.Add(activity, activity.ScheduleId)
        activity.Id = insertedId
    else:
        activityService.Update(activity)

    if changePos != -1:
        activityService.SetNewPos(changePos, activity.Id, activity.ScheduleId)

    return HttpResponseRedirect(f"/schedule/activity/{activity.ScheduleId}")

def getsuccessors(request, activity_id):
    newPosId = int(request.GET["newposid"])
    activityService = ActivityService
    # activityId = request.GET.get("activityid")
    successors = activityService.GetSuccessors(activity_id, newPosId)
    data = { 'successorCount' : len(successors) }
    
    return JsonResponse(data)

def deleteindex(request, activity_id):
    scheduleId = request.GET["schedule_id"]
    dependencyService = DependencyService
    # Need to check to see if there are dependencies related to this activity
    dependencies = dependencyService.GetByActivityId(activity_id)

    template = loader.get_template('activity/delete.html')
    context = { 'dependencies' : len(dependencies), 'scheduleId' : scheduleId, 'activityId' : activity_id }
    return HttpResponse(template.render(context, request))

def delete(request, activity_id):
    scheduleId = request.POST["schedule_id"]    
    activityService = ActivityService
    activityService.Delete(activity_id)    
    return HttpResponseRedirect(f"/schedule/activity/{scheduleId}")