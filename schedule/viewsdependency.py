from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader

from schedule.models import Dependency, DependencyService

def index(request, activity_id):
    dependencyService = DependencyService
    dependencies = dependencyService.GetByActivityId(activity_id)

    template = loader.get_template('dependency/index.html')
    context = { 'dependencies' : dependencies }
    return HttpResponse(template.render(context, request))

def detail(request, dependency_id):
    dependencyService = DependencyService
    dependency = None
    
    if dependency_id != 0:
        dependency = dependencyService.GetById(dependency_id)

    template = loader.get_template('dependency/detail.html')
    context = { 'dependency' : dependency }
    return HttpResponse(template.render(context, request))