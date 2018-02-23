from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader

from schedule.models import Dependency, DependencyService, Activity, ActivityService

def index(request, activity_id):
    scheduleId = request.GET["schedule_id"]
    dependencyService = DependencyService
    dependencies = dependencyService.GetByActivityId(activity_id)

    template = loader.get_template('dependency/index.html')
    context = { 'dependencies' : dependencies, 'scheduleId' : scheduleId }
    return HttpResponse(template.render(context, request))

def detail(request, dependency_id):
    dependencyService = DependencyService
    dependency = dependencyService.GetById(dependency_id)
    dependencyTypes = dependencyService.GetDependencyTypes()
    activityService = ActivityService
    predActivities = activityService.GetPredecessors(dependency_id, request.GET["schedule_id"])
    
    if dependency_id != 0:
        dependency = dependencyService.GetById(dependency_id)

    template = loader.get_template('dependency/detail.html')
    context = { 'dependency' : dependency, 'dependencyTypes' : dependencyTypes, 'predActivities' : predActivities }
    return HttpResponse(template.render(context, request))