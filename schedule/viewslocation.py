from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.http import Http404

from schedule.models import Location, LocationService

def index(request):
    template = loader.get_template('location/index.html')
    context = { 'locations' : '' }
    return HttpResponse(template.render(context, request))

def detail(request, location_id):
    locationService = LocationService
    location = Location
    
    if location_id != 0:
        location = locationService.GetById(location_id)

    template = loader.get_template('location/index.html')    

    context = { 'locations' : location }
    return HttpResponse(template.render(context, request))

def update(request):
    locationService = LocationService
    location =  Location
    location.Id = request.POST['id']
    #location.Schedule_id = request.POST['schedule_id']
    location.Lat = request.POST['id']
    location.Long = request.POST['id']

    if location.Id == 0:
        locationService.Add(location)
    else:
        locationService.Update(location)

    return HttpResponseRedirect("/schedule/location/" + location.Id)
