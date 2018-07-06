from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.conf import settings

from schedule.models import Dependency, DependencyService, Activity, ActivityService

def index(request, activity_id):
    scheduleId = request.GET["schedule_id"]
    dependencyService = DependencyService
    dependencies = dependencyService.GetByActivityId(activity_id)
    activityService = ActivityService
    activity = ActivityService.GetById(activity_id)
    demoMode = settings.DEMO_MODE

    template = loader.get_template('dependency/index.html')
    context = { 'dependencies' : dependencies, 'scheduleId' : scheduleId, 'activityId' : activity_id, 'activity' : activity, 'demoMode' : demoMode }
    return HttpResponse(template.render(context, request))

def detail(request, dependency_id):
    scheduleId = request.GET["schedule_id"]
    activityId = request.GET["activity_id"]
    demoMode = settings.DEMO_MODE

    dependencyService = DependencyService
    dependency = Dependency()

    if dependency_id != 0:
        dependency = dependencyService.GetById(dependency_id)

    dependencyTypes = dependencyService.GetDependencyTypes()
    activityService = ActivityService
    predActivities = activityService.GetPredecessors(activityId, scheduleId)
    activity = activityService.GetById(activityId)

    template = loader.get_template('dependency/detail.html')
    context = { 'dependency' : dependency, 'dependencyTypes' : dependencyTypes, 'predActivities' : predActivities, 
                'activityId' : activityId, 'scheduleId' : scheduleId, 'activity' : activity, 'demoMode' : demoMode }
    return HttpResponse(template.render(context, request))

def update(request, dependency_id):
    activityId = request.POST["activity_id"]
    scheduleId = request.POST["schedule_id"]
    dependencyService = DependencyService
    dependency = Dependency()

    dependency.Id = dependency_id
    dependency.ActivityId = activityId
    dependency.PredActivityId = request.POST["pred_activity_id"]
    dependency.DependencyTypeId = request.POST["dependency_type_id"]
    dependency.DependencyLength = request.POST["dependency_length"]

    if dependency.Id == 0:
        dependencyService.Add(dependency)
    else:
        dependencyService.Update(dependency)

    return HttpResponseRedirect(f"/schedule/dependency/{activityId}?schedule_id={scheduleId}")
    
def deleteindex(request, dependency_id):
    scheduleId = request.GET["schedule_id"]
    activityId = request.GET["activity_id"]

    template = loader.get_template('dependency/delete.html')
    context = { 'dependencyId' : dependency_id, 'scheduleId' : scheduleId, 'activityId' : activityId }
    return HttpResponse(template.render(context, request))

def delete(request, dependency_id):
    activityId = request.POST["activity_id"]
    scheduleId = request.POST["schedule_id"]

    dependencyService = DependencyService
    dependencyService.Delete(dependency_id)    

    return HttpResponseRedirect(f"/schedule/dependency/{activityId}?schedule_id={scheduleId}")
    