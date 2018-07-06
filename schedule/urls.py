from django.urls import path

from . import views
from . import viewslocation
from . import viewsactivity
from . import viewsdependency
from . import viewsreport

app_name = 'schedule'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:schedule_id>/', views.detail, name='detail'),
    path('<int:schedule_id>/update', views.update, name='update'),
    path('<int:schedule_id>/delete', views.delete, name='delete'),
    path('<int:schedule_id>/deleteindex', views.deleteindex, name='deleteindex'),
    path('location/<int:schedule_id>/index', viewslocation.index, name='index'),
    path('location/<int:location_id>/detail', viewslocation.detail, name='detail'),
    path('location/<int:location_id>/update', viewslocation.update, name='update'),
    path('location/<int:location_id>/delete', viewslocation.delete, name='delete'),
    path('location/<int:location_id>/deleteindex', viewslocation.deleteindex, name='deleteindex'),
    path('activity/<int:schedule_id>', viewsactivity.index, name='index'),
    path('activity/<int:activity_id>/detail', viewsactivity.detail, name='detail'),
    path('activity/<int:activity_id>/delete', viewsactivity.delete, name='delete'),
    path('activity/<int:activity_id>/update', viewsactivity.update, name='update'),
    path('activity/<int:activity_id>/deleteindex', viewsactivity.deleteindex, name='deleteindex'),
    path('activity/<int:activity_id>/getsuccessors', viewsactivity.getsuccessors, name='getsuccessors'),
    path('dependency/<int:activity_id>', viewsdependency.index, name='index'),
    path('dependency/<int:dependency_id>/detail', viewsdependency.detail, name='detail'),
    path('dependency/<int:dependency_id>/update', viewsdependency.update, name='update'),
    path('dependency/<int:dependency_id>/delete', viewsdependency.delete, name='delete'),
    path('dependency/<int:dependency_id>/deleteindex', viewsdependency.deleteindex, name='deleteindex'),
    path('report/<int:schedule_id>/', viewsreport.index, name='index'),
    path('reportdays/<int:schedule_id>/', viewsreport.daysindex, name='daysindex'),
    path('reportstochastic/<int:schedule_id>/', viewsreport.stochasticindex, name='stochasticindex'),
]