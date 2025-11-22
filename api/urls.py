from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = routers.DefaultRouter()

router.register('EventImages' , views.eventImageViewSet)
router.register('participantset' , views.participantViewSet)
router.register('subevents' , views.EventSubViewSet)
router.register('paymconfirminfo' , views.participantPaymViewSet)   

urlpatterns = [    
    #path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns = [
    path('', views.getRoutes , name='event-api-routes'),
    path('', include(router.urls) , name='event-api-eventimages'),
    path('events/', views.getEvents , name='event-api-events'),
    path('events/create/', views.createEvent , name='event-api-createevent'),
    path('events/<str:pk>/update/', views.updateEvent , name='event-api-updateevent'),
    path('events/<str:pk>/delete/', views.deleteEvent , name='event-api-deleteevent'),
    path('events/<str:pk>/', views.getEvent , name='event-api-event'),
    path('events/unregistered/<str:pk>/', views.getEventsUnregistered , name='event-api-event'),
    path('events/related/<str:pk>/', views.getEventRelated , name='event-api-event'),

    path('participants/', views.getParticipants , name='participant-api-events'),
    path('participants/create/', views.createParticipant , name='participant-api-createevent'),
    path('participants/<str:pk>/update/', views.updateParticipant , name='participant-api-updateevent'),
    path('participants/<str:pk>/delete/', views.deleteParticipant , name='participant-api-deleteevent'),
    path('participants/<str:pk>/', views.getParticipant , name='participant-api-event'),
    path('participants/check/<str:pk>/', views.getParticipantExists , name='participant-exists-api-event'),

    path('participantEvents/<str:pk>/', views.getParticipantEvents , name='participantEvents-api-events'),
    path('participantevents/create/', views.updateParticipantEvent , name='participantEvents-api-createevent'),
    path('participantevents/remove/', views.removeParticipantEvent , name='participantEvents-api-remove'),
    path('participantcompletedevents/<str:pk>/', views.getParticipantCompletedEvents , name='participantEvents-api-completed'),
    

    path('events/images/<int:pk>/', views.getEventImage , name='event-api-eventimage'),
    path('events/usableimages/<int:pk>/', views.getEventImageUsable , name='event-api-eventimageurl'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('getavashyaka/', views.getPayfastConnectionDetails , name='api-getavashyaka'),
    
    #path('eventdetails/', views.EventDetailListCreate.as_view() , name='event-details-create'),
]
