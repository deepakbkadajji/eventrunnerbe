from rest_framework import serializers 
from .models import AppSponsorTable
from .models import EventDetailTable
from .models import ParticipantTable
from .models import ParticipantPaymRefTable
from .models import ParticipantEventTable
from .models import EventImages
from .models import EventSubDetailTable
from .models import EventNotificationTable
from .models import EventSponsorTable
from .models import User


class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImages
        #fields = '__all__'
        fields = ['id' , 'event_id' , 'eventMainImg']

class EventSubDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='eventcategory.categoryname')

    class Meta:
        model = EventSubDetailTable
        fields = ['id' , 'event', 'name' , 'eventcategory' , 'category_name' , 'eventsubdate' , 'regfees' , 'regfeescurrency' ]

class EventNotificationSerializer(serializers.ModelSerializer):

    event_name = serializers.ReadOnlyField(source='event.eventname')

    class Meta:
        model = EventNotificationTable
        fields = ['id' , 'event' , 'title' , 'message' , 'notificationImg' , 'event_name']

class EventSponsorSerializer(serializers.ModelSerializer):
    event_name = serializers.ReadOnlyField(source='event.eventname')

    class Meta:
        model = EventSponsorTable
        fields = ['id' , 'event' , 'companyname' , 'description' , 'sponsorImg' , 'externallink' , 'event_name', 'sponsorcategory']

class EventDetailSerializer(serializers.ModelSerializer):
    #eventimgs = EventImageSerializer(many=False , read_only=True)
    #subeventsvar = EventSubDetailSerializer(source = 'EventSubDetailTable_set' , many=True , read_only=True )
    subevents = EventSubDetailSerializer(source = 'subevent_event' , many=True , read_only=True )
    eventimage = EventImageSerializer(source = 'eventimage_event' , many=False , read_only=True )
    eventnotifications = EventNotificationSerializer(source = 'eventnotification_event' , many=True , read_only=True )
    eventsponsors = EventSponsorSerializer(source = 'eventsponsor_event' , many=True , read_only=True )

    class Meta:
        model = EventDetailTable
        #fields = '__all__'
        #field = ['id' , 'eventid' , 'eventname' , 'updated' , 'created' ]
        #,'eventimgs' , 'eventid'
        fields = ['id' , 'eventid' ,'eventname','eventdate','eventenddate','updated','created','contactpersonname','contactpersonsurname','contactpersonothername','contactpersonemailaddr','contactpersonphonenum','eventstatus','contactpersoncitizenship','contactpersonnationality','contactpersonprovince','contactpersoncountry','contactpersonaddrtype','contactpersonaddr1','contactpersonaddr2','contactpersonaddr3','contactpersonaddr4','contactpersonaddrcode','terminationstatus','eventdescription','eventtype','eventcategory','startPointLat','startPointLng' , 'subevents' , 'eventimage' , 'eventnotifications', 'eventsponsors']



class ParticipantSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        model = ParticipantTable
        fields = '__all__'

class ParticipantPaymTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantPaymRefTable
        fields = '__all__'

class ParticipantEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantEventTable
        fields = '__all__'



class AppSponsorSerializer(serializers.ModelSerializer):
    event_name = serializers.ReadOnlyField(source='event.eventname')

    class Meta:
        model = AppSponsorTable
        fields = ['id' , 'companyname' , 'description' , 'sponsorImg' , 'externallink' , 'event_name', 'sponsorcategory']


