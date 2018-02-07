from django.urls import path

from . import views
from . import viewslocation

app_name = 'schedule'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:schedule_id>/', views.detail, name='detail'),
    path('<int:schedule_id>/update', views.update, name='update'),
    path('location/<int:schedule_id>/index', viewslocation.index, name='index'),
    path('location/<int:location_id>/detail', viewslocation.detail, name='detail'),
    path('location/update', viewslocation.update, name='update'),
]