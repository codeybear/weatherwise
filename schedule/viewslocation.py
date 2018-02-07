from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.http import Http404

from schedule.models import Location, LocationService

def index(request, schedule_id):
    locationService = LocationService
    locations = locationService.GetByScheduleId(schedule_id)    
    
    template = loader.get_template('location/index.html')
    context = { 'locations' : locations, 'viewtype' : 'index' }
    return HttpResponse(template.render(context, request))

def detail(request, location_id):
    locationService = LocationService
    location = Location
    
    if location_id != 0:
        location = locationService.GetById(location_id)

    template = loader.get_template('location/index.html')    

    context = { 'location' : location, 'viewtype' : 'detail' }
    return HttpResponse(template.render(context, request))

def update(request):
    locationService = LocationService
    location =  Location
    location.Id = request.POST['id']
    location.ScheduleId = request.POST['schedule_id']
    location.Name = request.POST['name']
    location.Lat = request.POST['lat']
    location.Long = request.POST['long']

    if location.Id == 0:
        locationService.Add(location)
    else:
        locationService.Update(location)

    return HttpResponseRedirect(f"/schedule/location/{location.ScheduleId}/index")
