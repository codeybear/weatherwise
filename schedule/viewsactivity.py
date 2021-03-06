from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.template import loader

from schedule.models import Activity, ActivityService, LocationService, DependencyService


def index(request, schedule_id):
    activityService = ActivityService
    activities = activityService.GetByScheduleId(schedule_id)
    demoMode = settings.DEMO_MODE

    template = loader.get_template('activity/index.html')
    context = {'activities': activities, 'viewtype': 'index', 'scheduleId': schedule_id, 'demoMode': demoMode}
    return HttpResponse(template.render(context, request))


def detail(request, activity_id):
    scheduleId = request.GET["schedule_id"]
    activityService = ActivityService
    activities = activityService.GetByScheduleId(scheduleId)
    activity = Activity()
    locationService = LocationService
    demoMode = settings.DEMO_MODE

    if activity_id != 0:
        activity = ActivityService.GetById(activity_id)
    else:
        activity.Id = 0

    locations = locationService.GetByScheduleId(scheduleId)
    activityTypes = activityService.GetActivityTypes()

    template = loader.get_template('activity/detail.html')
    context = {'activity': activity, 'locations': locations, 'activitytypes': activityTypes, 'viewtype': 'detail',
               'scheduleId': scheduleId, 'activities': activities, 'demoMode': demoMode}

    return HttpResponse(template.render(context, request))


def update(request, activity_id):
    changePos = int(request.POST["selectPosition"])
    activityService = ActivityService
    activity = Activity()

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
    successors = activityService.GetSuccessors(activity_id, newPosId)
    data = {'successorCount': len(successors)}

    return JsonResponse(data)


def deleteindex(request, activity_id):
    scheduleId = request.GET["schedule_id"]
    dependencyService = DependencyService
    # Need to check to see if there are dependencies related to this activity
    dependencies = dependencyService.GetByActivityId(activity_id)
    predDependencies = dependencyService.GetPredByActivityId(activity_id)
    dependencyCount = len(dependencies) + len(predDependencies)

    template = loader.get_template('activity/delete.html')
    context = {'dependencyCount': dependencyCount, 'scheduleId': scheduleId, 'activityId': activity_id}
    return HttpResponse(template.render(context, request))


def delete(request, activity_id):
    scheduleId = request.POST["schedule_id"]
    activityService = ActivityService
    activityService.Delete(activity_id)
    return HttpResponseRedirect(f"/schedule/activity/{scheduleId}")
