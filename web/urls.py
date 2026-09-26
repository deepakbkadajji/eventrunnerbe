from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('userhome/', views.userhome, name='userhome'),
    path('administrator/', views.administrator, name='administrator'),
    path(
        'athletic-associations/',
        views.athletic_associations,
        name='athletic_associations'
    ),
    path(
        'athletic-organisations/',
        views.athletic_organisations,
        name='athletic_organisations'
    ),
    path(
        'athletic-organisations/<int:id>/',
        views.athletic_organisation_details,
        name='athletic_organisation_details'
    ),
    path('about/', views.about, name='about'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('policy/', views.public_policy, {'document_type': 'app'}, name='public_policy'),
    path(
        'policy/version/<int:id>/',
        views.public_policy_version,
        name='public_policy_version',
    ),
    path(
        'policy/<str:document_type>/',
        views.public_policy,
        name='public_policy_by_type',
    ),
    path('events/', views.events, name='events'),
    path('organisations/', views.organisations, name='organisations'),
    path(
        'organisations/<int:id>/',
        views.organisation_details,
        name='organisation_details'
    ),
    path('events/new-event/', views.new_event, name='new_event'),
    path('events/new/', views.event_create, name='event_create'),
    path(
        'events/<int:id>/', 
        views.event_details, 
        name='event_details'),
    path(
        'events-edit/<int:id>/', 
        views.event_details_edit, 
        name='event_details_edit'),
    #path("login2/", views.login_view, name="login"),
    path(
        'events/edit/<int:id>/', 
        views.event_details_editpage, 
        name='event_details_editpage'),
    path(
        'events/new/', 
        views.event_details_newpage, 
        name='event_details_newpage'),
    path(
        'participants/',
        views.participants,
        name='participants'
    ),

    path(
        'participants/<int:id>/',
        views.participant_details,
        name='participant_details'
    ),
    path(
        'participants/edit/<int:id>/',
        views.participant_details_edit,
        name='participant_details_edit'
    ),
    path(
        'event_participants/<int:id>/', 
        views.event_participants, 
        name='event_participants'),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='website/login.html'
        ),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(
            next_page='login'
        ),
        name='logout'
    ),
    path("whoami/", views.whoami, name="whoami"),
]