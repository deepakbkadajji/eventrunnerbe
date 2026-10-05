from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.urls import path
from .views import users


router = routers.DefaultRouter()

router.register('EventImages' , views.eventImageViewSet)
router.register('participantset' , views.participantViewSet)
router.register('subevents' , views.EventSubViewSet)
router.register('paymconfirminfo' , views.participantPaymViewSet)   
router.register('eventmodel' , views.eventViewSet , basename='eventmodel')
router.register('eventnotifications' , views.EventNotificationViewSet)
router.register('organisationnotifications', views.OrganisationNotificationViewSet)
router.register('appnotifications', views.AppNotificationViewSet)
router.register('eventsponsors' , views.EventSponsorViewSet)
router.register('appsponsors' , views.AppSponsorViewSet)
router.register('eventinformation' , views.eventInfoViewSet)
router.register('organisations' , views.OrganisationViewSet)
router.register('organisationmembers' , views.OrganisationMemberViewSet)
router.register('organisationevents' , views.OrganisationEventViewSet)
router.register('athleticorganisations' , views.AthleticOrganisationViewSet)
router.register('athleticorganisationmembers' , views.AthleticOrganisationMemberViewSet)
router.register('athleticorganisationcategories' , views.AthleticOrganisationCategoryViewSet)
router.register('errorreports', views.ErrorViewSet)
router.register('appreleaseversions', views.AppReleaseVersionViewSet)
router.register('termsandconditions', views.TermsAndConditionsViewSet)

#router.register('eventdetails' , views.EventsDetailsView , basename='eventdetails')

urlpatterns = [
    path(
        'participantset/lookup-by-email/',
        views.participantViewSet.as_view({'post': 'lookup_by_email'}),
        name='participant-lookup-by-email',
    ),
    path(
        'appreleaseversions/lookup/',
        views.AppReleaseVersionViewSet.as_view({'post': 'lookup'}),
        name='app-release-version-lookup',
    ),
    path(
        'termsandconditions/current/',
        views.TermsAndConditionsViewSet.as_view({'get': 'current', 'post': 'current'}),
        name='terms-current',
    ),
    path('terms/current/', views.getCurrentTerms, name='terms-current-alias'),
    path('terms/status/', views.getParticipantTermsStatus, name='terms-status'),
    path('terms/accept/', views.acceptParticipantTerms, name='terms-accept'),
    path(
        'notification-reads/inbox/',
        views.listParticipantNotificationInbox,
        name='notification-read-inbox',
    ),
    path(
        'notification-reads/event-unread/',
        views.listUnreadEventNotifications,
        name='notification-read-event-unread',
    ),
    path(
        'notification-reads/event-notifications/',
        views.listEventNotificationsForParticipant,
        name='notification-read-event-notifications',
    ),
    path('notification-reads/mark/', views.markNotificationRead, name='notification-read-mark'),
    path('notification-reads/list/', views.listNotificationReads, name='notification-read-list'),
    path('notification-reads/status/', views.getNotificationReadStatus, name='notification-read-status'),
    path(
        'notification-reads/unread-count/',
        views.getNotificationUnreadCount,
        name='notification-read-unread-count',
    ),
    path('', views.getRoutes , name='event-api-routes'),
    path('', include(router.urls) , name='event-api-eventimages'),
    path('events/', views.getEvents , name='event-api-events'),
    path('events/list/', views.getEventsList , name='event-api-events-list'),
    path('events/cards/registered-upcoming/', views.getParticipantRegisteredUpcomingEventCards, name='event-api-cards-registered-upcoming'),
    path('events/cards/available-upcoming/', views.getParticipantAvailableUpcomingEventCards, name='event-api-cards-available-upcoming'),
    path('events/cards/completed-past/', views.getParticipantCompletedPastEventCards, name='event-api-cards-completed-past'),
    path(
        'events/club-completed/',
        views.getClubCompletedClosedEvents,
        name='event-api-club-completed-closed',
    ),
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

    path('subevents_event/<str:pk>/', views.getSubeventsEvent , name='api-getsubevents_events'),
    path('event_participants/<str:pk>/', views.getEventsParticipant , name='api-getparticipants_event'),
    
    
    path('getavashyaka/', views.getPayfastConnectionDetails , name='api-getavashyaka'),
    
    path('participants_import/', views.ParticipantImportView.as_view(), name='participants-import-api'),

    path('athleticorganisations/tree/', views.athleticOrganisationTree, name='athletic-organisation-tree'),
    path('athleticorganisations/add_root/', views.athleticOrganisationAddRoot, name='athletic-organisation-add-root'),
    path('athleticorganisations/add_child/', views.athleticOrganisationAddChild, name='athletic-organisation-add-child'),
    path('athleticorganisations/move/', views.athleticOrganisationMove, name='athletic-organisation-move'),
    path('athleticorganisations/update/', views.athleticOrganisationUpdateNode, name='athletic-organisation-update'),
    path('athleticorganisations/delete/', views.athleticOrganisationDeleteNode, name='athletic-organisation-delete'),
    
    #path('eventdetails/', views.EventDetailListCreate.as_view() , name='event-details-create'),

    path('users/', users),
]


