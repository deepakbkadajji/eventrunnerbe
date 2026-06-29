from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('userhome/', views.userhome, name='userhome'),
    path('about/', views.about, name='about'),
    path('events/', views.events, name='events'),
    path('events/new-event/', views.new_event, name='new_event'),
    path(
        'events/<int:id>/', 
        views.event_details, 
        name='event_details'),
    #path("login2/", views.login_view, name="login"),
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