from rest_framework import serializers 
from .models import EventDetailTable
from .models import ParticipantTable
from .models import ParticipantPaymRefTable
from .models import ParticipantEventTable
from .models import EventImages
from .models import EventSubDetailTable

class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImages
        #fields = '__all__'
        fields = ['id' , 'event_id' , 'eventMainImg']

class EventSubDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventSubDetailTable
        fields = '__all__'

class EventDetailSerializer(serializers.ModelSerializer):
    #eventimgs = EventImageSerializer(many=False , read_only=True)
    subevents = EventSubDetailSerializer(source = 'EventSubDetailTable_set' , many=True , read_only=True )

    class Meta:
        model = EventDetailTable
        #fields = '__all__'
        #field = ['id' , 'eventid' , 'eventname' , 'updated' , 'created' ]
        #,'eventimgs' , 'eventid'
        fields = ['id' , 'eventid' ,'eventname','eventdate','eventenddate','updated','created','contactpersonname','contactpersonsurname','contactpersonothername','contactpersonemailaddr','contactpersonphonenum','eventstatus','contactpersoncitizenship','contactpersonnationality','contactpersonprovince','contactpersoncountry','contactpersonaddrtype','contactpersonaddr1','contactpersonaddr2','contactpersonaddr3','contactpersonaddr4','contactpersonaddrcode','terminationstatus','eventdescription','eventtype','eventcategory','startPointLat','startPointLng' , 'subevents']



class ParticipantSerializer(serializers.ModelSerializer):
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

