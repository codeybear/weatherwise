from django.urls import path

from . import views
from . import viewslocation
from . import viewsactivity

app_name = 'schedule'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:schedule_id>/', views.detail, name='detail'),
    path('<int:schedule_id>/update', views.update, name='update'),
    path('location/<int:schedule_id>/index', viewslocation.index, name='index'),
    path('location/<int:location_id>/detail', viewslocation.detail, name='detail'),
    path('location/<int:location_id>/update', viewslocation.update, name='update'),
    path('activity/<int:schedule_id>/index', viewsactivity.index, name='index'),
    path('activity/<int:activity_id>/detail', viewsactivity.detail, name='detail'),
]