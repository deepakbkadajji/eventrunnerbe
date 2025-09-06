from rest_framework import serializers 
from .models import EventDetailTable
from .models import ParticipantTable
from .models import EventImages

class EventDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventDetailTable
        fields = '__all__'
        #field = ['id' , 'eventid' , 'eventname' , 'updated' , 'created' ]
        #fields = ['id' , 'eventid' , 'eventname' , 'eventdate' , 'updated' , 'created' , 'contactpersonname' , 'contactpersonsurname' , 'eventstatus' , 'eventdescription' , 'eventtype' , 'eventcategory']

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantTable
        fields = '__all__'

class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImages
        #fields = '__all__'
        fields = ['id' , 'event_id' , 'eventMainImg']