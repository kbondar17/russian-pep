from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from appointments.views.person import PersonDetail
from django.conf.urls.static import static

from appointments.views.persons_table import PersonsList 
from appointments.views.events_views import EventList, EventDetail

app_name = 'appointments' 

urlpatterns = [

    path('person/<int:pk>', PersonDetail.as_view(), name='person-detail'),
    path('person_all/', PersonsList.as_view(), name='person-list'),
    path('person_all/<str:query>', PersonsList.as_view(), name='person-list-query'),

    path('events/<int:pk>', EventDetail.as_view(), name='event-detail'),
    path('events/<str:query>', EventList.as_view(), name='show-all-events',),
    path('events/', EventList.as_view(), name='show-all-events',),


]

urlpatterns += staticfiles_urlpatterns()

