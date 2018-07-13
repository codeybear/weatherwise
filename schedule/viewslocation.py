from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.http import Http404
from django.conf import settings

from schedule.models import Location, LocationService, Activity, ActivityService

def index(request, schedule_id):
    locationService = LocationService
    locations = locationService.GetByScheduleId(schedule_id)    
    demoMode = settings.DEMO_MODE

    template = loader.get_template('location/index.html')
    context = { 'locations' : locations, 'viewtype' : 'index', 'scheduleId' : schedule_id, 'demoMode' : demoMode }
    return HttpResponse(template.render(context, request))

def detail(request, location_id):
    locationService = LocationService
    location = Location()
    scheduleId = request.GET['schedule_id']
    demoMode = settings.DEMO_MODE
    
    if location_id != 0:
        location = locationService.GetById(location_id)

    template = loader.get_template('location/index.html')    
    context = { 'location' : location, 'viewtype' : 'detail', 'scheduleId' : scheduleId, 'demoMode' : demoMode }
    return HttpResponse(template.render(context, request))

def update(request, location_id):
    locationService = LocationService
    location =  Location()
    location.Id = int(request.POST['id'])
    location.ScheduleId = request.POST['schedule_id']
    location.Name = request.POST['name']
    location.Lat = request.POST['lat']
    location.Long = request.POST['long']

    if location.Id == 0:
        locationService.Add(location)
    else:
        locationService.Update(location)

    return HttpResponseRedirect(f"/schedule/location/{location.ScheduleId}/index")

def deleteindex(request, location_id):
    scheduleId = request.GET["schedule_id"]
    activityService = ActivityService

    # Need to check to see if there are dependencies related to this activity
    activities = activityService.GetByLocationId(location_id)

    template = loader.get_template('location/delete.html')
    context = { 'activities' : len(activities), 'scheduleId' : scheduleId, 'locationId' : location_id }
    return HttpResponse(template.render(context, request))

def delete(request, location_id):
    scheduleId = request.POST["schedule_id"]    
    locationService = LocationService
    locationService.Delete(location_id)    
    return HttpResponseRedirect(f"/schedule/location/{scheduleId}/index")
    