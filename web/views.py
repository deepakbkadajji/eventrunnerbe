from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from api.models import ParticipantTable
from api.models import EventDetailTable

# Create your views here.
def home(request):
    return render(request, 'website/home.html')

def about(request):
    return render(request, 'website/about.html')

@login_required
def userhome(request):
    return render(request, 'website/userhome.html')

@login_required
def events(request):
    return render(request, 'website/events.html')

@login_required
def new_event(request):
    return render(request, 'website/new-event.html')
    
@login_required
def event_details(request, id):
    #return render(request, 'website/event-details.html')  

    event = EventDetailTable.objects.get(
        id=id
    )

    return render(
        request,
        "website/event-details.html",
        {
            "event": event
        }
    )

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("home")

        return render(
            request,
            "website/login.html",
            {
                "error": "Invalid username or password."
            }
        )

    return render(request, "website/login.html")

@login_required
def logout_view(request):

    logout(request)

    return redirect('/login')

@login_required
def participants(request):

    participants = ParticipantTable.objects.all()

    return render(
        request,
        "website/participants.html",
        {
            "participants": participants
        }
    )

@login_required
def participant_details(request, id):

    participant = ParticipantTable.objects.get(
        id=id
    )

    return render(
        request,
        "website/participant-details.html",
        {
            "participant": participant
        }
    )

@login_required
def whoami(request):
    return JsonResponse({
        "authenticated": request.user.is_authenticated,
        "username": request.user.username if request.user.is_authenticated else None
    })