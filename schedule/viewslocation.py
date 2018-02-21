from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.http import Http404

from schedule.models import Location, LocationService, Activity, ActivityService

def index(request, schedule_id):
    locationService = LocationService
    locations = locationService.GetByScheduleId(schedule_id)    
    
    template = loader.get_template('location/index.html')
    context = { 'locations' : locations, 'viewtype' : 'index', 'ScheduleId' : schedule_id }
    return HttpResponse(template.render(context, request))

def detail(request, location_id):
    locationService = LocationService
    location = Location()
    
    if location_id != 0:
        location = locationService.GetById(location_id)
    else:
        location.ScheduleId = request.GET['schedule_id']    # If this is an insert then schedule_id will be supplied in the query string

    template = loader.get_template('location/index.html')    
    context = { 'location' : location, 'viewtype' : 'detail' }
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
    activityService = activityService

    # Need to check to see if there are dependencies related to this activity
    activities = activityService.GetByLocationId(location_id)

    template = loader.get_template('location/delete.html')
    context = { 'activities' : len(activities), 'scheduleId' : scheduleId, 'locationId' : location_id }
    return HttpResponse(template.render(context, request))

def delete(request, location_id):
    scheduleId = request.POST["schedule_id"]    
    locationService = locationService
    locationService.Delete(location_id)    
    return HttpResponseRedirect(f"/schedule/activity/{scheduleId}")