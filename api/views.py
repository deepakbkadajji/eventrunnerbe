from django.contrib.auth.models import User

from django.shortcuts import render
from rest_framework import generics

from .serializers import EventDetailSerializer
from .models import EventDetailTable

from .serializers import EventSubDetailSerializer
from .models import EventSubDetailTable

from .serializers import ParticipantSerializer
from .models import ParticipantTable

from .serializers import ParticipantPaymTableSerializer
from .models import ParticipantPaymRefTable

from .serializers import EventImageSerializer
from .models import EventImages

from .models import ParticipantEventTable

from .util import EventStatus
from django.db.models import Q

import os
from decouple import config

from django.db import transaction

#from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet 



#from eventrunnerbe.utils import customTokenBackend

#from eventrunnerbe.utils import CustomJWTAuthentication



from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
#from multipart import MultipartParser
#from multipart import Form

from functools import wraps

import jwt

import json
import requests

from django.http import JsonResponse

import boto3
from django.conf import settings



def generate_s3_presigned_url(object_key, expiration=600):
    """
    Generates a presigned URL for an S3 object.

    Args:
        object_key (str): The key (path) of the object in the S3 bucket.
        expiration (int): The duration in seconds for which the presigned URL is valid.
                          Defaults to 3600 seconds (1 hour).

    Returns:
        str: The presigned URL, or None if an error occurs.
    """
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME # Ensure this is defined in your settings.py
    )
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': object_key},
            ExpiresIn=expiration
        )
        return response
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        return None

def get_token_auth_header(request):
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    #print(auth)
    parts = auth.split()
    token = parts[1]

    return token

def jwt_decode_token(token):
    header = jwt.get_unverified_header(token)
    jwks = requests.get('https://{}/.well-known/jwks.json'.format('dev-x8hbr3jrn2mxvw4x.us.auth0.com')).json()
    public_key = None
    for jwk in jwks['keys']:
        if jwk['kid'] == header['kid']:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception('Public key not found.')

    issuer = 'https://{}/'.format('dev-x8hbr3jrn2mxvw4x.us.auth0.com')
    return jwt.decode(token, public_key, audience='https://eventrunner.com/api/', issuer=issuer, algorithms=['RS256'])

def requires_scope(required_scope):
    """Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """
    def require_scope(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_auth_header(args[0])
            #print(token)   
            
            decoded = jwt_decode_token(token)  
            #print(decoded)  

            #decoded = jwt.decode(token, verify=False , algorithms=['RS256'])
            if decoded.get("scope"):
                token_scopes = decoded["scope"].split()
                for token_scope in token_scopes:
                    if token_scope == required_scope:
                        return f(*args, **kwargs)
            response = JsonResponse({'message': 'You don\'t have access to this resource'})
            response.status_code = 403
            return response
        return decorated
    return require_scope


#class EventDetailListCreate(generics.ListCreateAPIView)
#    queryset = EventDetailTable.objects.all()
#    serializer_class = eventdetailserializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint' : '/events/',
            'method' : 'GET',
            'body' : None,            
            'description' : 'Returns an array of events'
        },
        {
            'Endpoint' : '/events/id',
            'method' : 'GET',
            'body' : None,            
            'description' : 'Returns a single event'
        }
    ]
    return Response(routes)

##### Event details
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getEvents(request):
    eventdetails = EventDetailTable.objects.all()
    eventserializer = EventDetailSerializer(eventdetails , many=True)
    return  Response(eventserializer.data)

@api_view(['GET'])
#@requires_scope('read:events')
def getEvent(request , pk):
    eventdetail = EventDetailTable.objects.get(id = pk)
    eventserializer = EventDetailSerializer(eventdetail , many=False)
    return  Response(eventserializer.data)

@api_view(['GET'])
#@requires_scope('read:events')
def getEventRelated(request , pk):
    eventdetail = EventDetailTable.objects.get(id = pk)
    #eventImages = EventDetailTable.objects.select_related('event')
    #if eventImages.count() == 0:
    #    print('querysetempty')

    eventImg =  EventImages.objects.select_related('event').all()

    #if eventdetail2.count() != 0:
    #    return  Response('Event images')
    #else:
    #    return  Response('No event images')
    eventImgserializer = EventImageSerializer(eventImg , many=True)
    #eventserializer = EventDetailSerializer(eventdetail2 , many=True)
    
    return  Response(eventImgserializer.data)

@api_view(['POST'])
#@requires_scope('create:event')
def createEvent(request):
    data = request.data
    eventdetail = EventDetailTable.objects.create(
        eventid = data['eventid'],
        eventname = data['eventname'],
        contactpersonname = data['contactpersonname'],
        contactpersonsurname = data['contactpersonsurname'],
        eventstatus = data['eventstatus'],
        eventdescription = data['eventdescription'],
        eventtype = data['eventtype'],
        eventcategory = data['eventcategory']
    )
    eventserializer = EventDetailSerializer(eventdetail , many=False)
    return  Response(eventserializer.data)

@api_view(['PUT'])
#@requires_scope('update:event')
def updateEvent(request , pk):
    data = request.data
    eventdetail = EventDetailTable.objects.get(id = pk)
    eventserializer = EventDetailSerializer(eventdetail , data=request.data)
    if eventserializer.is_valid():
        eventserializer.save()    
    return  Response(eventserializer.data)

@api_view(['DELETE'])
#@requires_scope('delete:event')
def deleteEvent(request , pk):
    eventdetail = EventDetailTable.objects.get(id = pk)
    eventdetail.delete()  
    return  Response("Event was deleted")

@api_view(['GET'])
#@requires_scope('read:events')
def getEventsUnregistered(request , pk):
    participantdetail = ParticipantTable.objects.get(id = pk)
    #eventparticipantsdetail = participantdetail.events.all().values('id')
    eventlist = ParticipantEventTable.objects.filter(participant=participantdetail).filter(paymref__payment_status='Completed').values('event')
    eventdetail = EventDetailTable.objects.exclude(id__in=eventlist).exclude(Q(eventstatus=EventStatus.Completed) | Q(eventstatus=EventStatus.Closed)).order_by('eventdate')

    

    eventserializer = EventDetailSerializer(eventdetail , many=True)
    return  Response(eventserializer.data)

##### Participants
@api_view(['GET'])
#@requires_scope('read:profile')
def getParticipants(request):
    participantdetails = ParticipantTable.objects.all()
    participantserializer = ParticipantSerializer(participantdetails , many=True)
    return  Response(participantserializer.data)

@api_view(['GET'])
#@requires_scope('read:profile')
def getParticipant(request , pk):
    participantdetail = ParticipantTable.objects.get(id = pk)
    participantserializer = ParticipantSerializer(participantdetail , many=False)
    return  Response(participantserializer.data)

@api_view(['GET'])
#@requires_scope('read:profile')
def getParticipantExists(request , pk):
    participantdetail = ParticipantTable.objects.get(id = pk)
    participantserializer = ParticipantSerializer(participantdetail , many=False)

    if (participantdetail.authid):
        return Response("Participant exists" , HttpStatus=status.HTTP_200_OK)
    else:
        return Response("Participant does not exist" , status=status.HTTP_204_NO_CONTENT)   

@api_view(['POST'])
#@requires_scope('create:profile')
def createParticipant(request):
    data = request.data
    print(data)
    participantdetail = ParticipantTable.objects.create(
        user = data['user'],
        title = data['title'],
        surname = data['surname'],
        firstname = data['firstname'],
        othernames = data['othernames'],
        initials = data['initials'],
        preferredname = data['preferredname'],
        homelanguage = data['homelanguage'],
        preferredlanguage = data['preferredlanguage'],
        maidenname = data['maidenname'],
        countryofissue = data['countryofissue'],
        typefld = data['typefld'],
        disabled = data['disabled']
    )
    participantserializer = ParticipantSerializer(participantdetail , many=False)
    return  Response(participantserializer.data)

@api_view(['PUT'])
#@requires_scope('update:profile')
def updateParticipant(request , pk):
    data = request.data
    participantdetail = ParticipantTable.objects.get(id = pk)
    participantserializer = ParticipantSerializer(participantdetail , data=request.data)
    if participantserializer.is_valid():
        participantserializer.save()    
    return  Response(participantserializer.data)

@api_view(['DELETE'])
#@requires_scope('delete:profile')
def deleteParticipant(request , pk):
    participantdetail = ParticipantTable.objects.get(id = pk)
    participantdetail.delete()  
    return  Response("Participant was deleted")

##### Participants  events
@api_view(['GET'])
#@requires_scope('read:events')
def getParticipantEvents(request, pk):
    participantdetail = ParticipantTable.objects.get(id = pk)
    
    #eventdetails = participantdetail.events.filter(eventstatus__in=[EventStatus.RegistrationOpen, EventStatus.RegistrationClosed])  
    #eventdetails.order_by('eventdate') 
    #eventserializer = EventDetailSerializer(eventdetails , many=True)


    eventlist = ParticipantEventTable.objects.filter(participant=participantdetail).filter(paymref__payment_status='Completed').values('event')

    eventRegDetails = EventDetailTable.objects.filter(id__in=eventlist).filter(eventstatus__in=[EventStatus.RegistrationOpen, EventStatus.RegistrationClosed]).order_by('eventdate')
    eventserializer = EventDetailSerializer(eventRegDetails , many=True)
    return Response(eventserializer.data)

@api_view(['GET'])
#@requires_scope('read:events')
def getParticipantCompletedEvents(request, pk):
    participantdetail = ParticipantTable.objects.get(id = pk)
    #eventdetails = participantdetail.events.filter(eventstatus__in=[EventStatus.Closed, EventStatus.Completed])   
    #eventserializer = EventDetailSerializer(eventdetails , many=True)

    eventlist = ParticipantEventTable.objects.filter(participant=participantdetail).filter(paymref__payment_status='Completed').values('event')

    eventRegDetails = EventDetailTable.objects.filter(id__in=eventlist).filter(eventstatus__in=[EventStatus.Closed, EventStatus.Completed]).order_by('-eventdate')
    eventserializer = EventDetailSerializer(eventRegDetails , many=True)

    return Response(eventserializer.data)

@api_view(['POST'])
#@requires_scope('update:participant')
def updateParticipantEvent(request):
    data = request.data
    
    participantdetail = ParticipantTable.objects.get(id = data['user'])
    eventdetail = EventDetailTable.objects.get(id = data['event'])
    participantdetail.events.add(eventdetail)  
    return  Response("Participant was enrolled to the event")

@api_view(['POST'])
#@requires_scope('update:event')
def removeParticipantEvent(request):
    data = request.data
    
    participantdetail = ParticipantTable.objects.get(id = data['user'])
    eventdetail = EventDetailTable.objects.get(id = data['event'])
    participantdetail.events.remove(eventdetail)  
    return  Response("Participant was disenrolled to the event")

##### Events images
@api_view(['GET'])
def getEventImage(request , pk):
    #eventDet = EventDetailTable.objects.get(id = pk)
    eventimages = EventImages.objects.filter(event=pk)
    if eventimages.count():
        respResult = "Count is not zero"
    else:
        respResult = "Count is zero"

    for obj in eventimages:
        print(obj)  # Access attributes of the model instance

    eventimgserializer = EventImageSerializer(eventimages , many=True)
    #return  Response(eventimgserializer.data)
    return  Response(eventimgserializer.data)

##### Events images
@api_view(['GET'])
def getEventImageUsable(request , pk):
    #eventDet = EventDetailTable.objects.get(id = pk)
    eventimages = EventImages.objects.filter(event=pk)
    if eventimages.count():
        respResult = "Count is not zero"
    else:
        respResult = "Count is zero"

    for obj in eventimages:
        print(obj)  # Access attributes of the model instance
        
        presigned_url = generate_s3_presigned_url('media/public/' + obj.eventMainImg.name)

        data = [
            {            
                'id': obj.id,
                'event': obj.event.id,
                'eventMainImg': presigned_url if presigned_url else None
            }
        ]

    return  Response(data , status=status.HTTP_200_OK)

             
class eventImageViewSet(ModelViewSet):
    queryset = EventImages.objects.all()
    serializer_class = EventImageSerializer
    parser_classes = (MultiPartParser , FormParser)

    def create(self , request  , *args, **kwargs):
        event = request.data['event']
        eventDetTable = EventDetailTable.objects.get(id = event)

        eventMainImg = request.data['eventMainImg']
        eventImg = EventImages.objects.filter(event=event)
        if (eventImg.count() != 0):
            eventImg.delete()

        EventImages.objects.create(event = eventDetTable , eventMainImg = eventMainImg)            

        return Response("Event image uploaded successfully" , status = 201)    
    
    def retrieve(self , request  , *args, **kwargs):
        event = request.data['event']
        eventDetTable = EventDetailTable.objects.get(id = event)        
        eventImg = EventImages.objects.filter(event=event)
   
        eventimgserializer = EventImageSerializer(eventImg , many=True)
        return Response(eventimgserializer.data)    

    
class participantCheckViewSet(ModelViewSet):
    queryset = ParticipantTable.objects.all()
    serializer_class = ParticipantSerializer
    parser_classes = (MultiPartParser , FormParser , JSONParser)

    def retrieve(self , request  , *args, **kwargs):
        participantAuthid = request.data['authid']
        reqType = request.data['requesttype']  
        
        participant = ParticipantTable.objects.get(authid = participantAuthid) 
        if  reqType == 'check':
            if (participant.authid):
                return Response("Participant exists" , HttpStatus=status.HTTP_200_OK)
            else:
                return Response("Participant does not exist" , status=status.HTTP_204_NO_CONTENT)   
        else:
            participantserializer = ParticipantSerializer(participant , many=False)
            return  Response(participantserializer.data, HttpStatus=status.HTTP_200_OK)
        
    def list(self , request  , *args, **kwargs):
        participantAuthid = request.data['authid']
        reqType = request.data['requesttype']  
        
        try:
            participant = ParticipantTable.objects.get(authid = participantAuthid)
        except ParticipantTable.DoesNotExist:
            return Response("")

        if  reqType == 'check':
            return  Response(participant.id)
        else:
            participantserializer = ParticipantSerializer(participant , many=False)
            return  Response(participantserializer.data)
        
class participantViewSet(ModelViewSet):
    queryset = ParticipantTable.objects.all()
    serializer_class = ParticipantSerializer
    parser_classes = (MultiPartParser , FormParser , JSONParser)

    def retrieve(self , request  , *args, **kwargs):
        participantAuthid = request.data['authid']
        reqType = request.data['requesttype']  
        
        participant = ParticipantTable.objects.get(authid = participantAuthid) 
        if  reqType == 'check':
            if (participant.authid):
                return Response("Participant exists" , status=status.HTTP_200_OK)
            else:
                return Response("Participant does not exist" , status=status.HTTP_204_NO_CONTENT)   
        else:
            participantserializer = ParticipantSerializer(participant , many=False)
            return  Response(participantserializer.data, status=status.HTTP_200_OK)
        
    def list(self , request  , *args, **kwargs):


        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode) 
        participantAuthid = body['authid']
        reqType = body['reqtype'] 

        try:
            participant = ParticipantTable.objects.get(authid = participantAuthid)
        except ParticipantTable.DoesNotExist:
            return Response("", status=status.HTTP_204_NO_CONTENT)

        if  reqType == 'check':
            return  Response(participant.id, status=status.HTTP_200_OK)
        else:
            participantserializer = ParticipantSerializer(participant , many=False)
            return  Response(participantserializer.data, status=status.HTTP_200_OK)
        
    def create(self , request  , *args, **kwargs):

        try:
            participanrExists = ParticipantTable.objects.get(authid= request.data['authid'])   
            return Response(participanrExists.id, status=status.HTTP_200_OK)
        except ParticipantTable.DoesNotExist:
            pass

        try:
            usrname = request.data["user"]
            usr = User.objects.get(username= usrname)             
        except User.DoesNotExist:
            return Response("", status=status.HTTP_409_CONFLICT)
        
        participantTable = ParticipantTable.objects.create(
            user = usr,
            title = request.data['title'],
            surname = request.data['surname'],
            firstname = request.data['firstname'],
            othernames = request.data['othernames'],
            initials = request.data['initials'],
            preferredname = request.data['preferredname'],
            homelanguage = request.data['homelanguage'],
            preferredlanguage = request.data['preferredlanguage'],
            maidenname = request.data['maidenname'],
            countryofissue = request.data['countryofissue'],
            typefld = request.data['typefld'],
            emailaddress = request.data['emailaddress'],
            usrphonenum = request.data['usrphonenum'],
            authid = request.data['authid']
        )      

        reqData = request.data

        print(reqData)

        participantserializer = ParticipantSerializer(participantTable , many=False)
        return  Response(participantserializer.data , status=status.HTTP_201_CREATED)
    
    def update(self , request  , *args, **kwargs):
        participantId = request.data['id']
        participantTable = ParticipantTable.objects.get(id = participantId)        

        reqData = request.data

        print(reqData)

        for reqAttr in request.data:
            if reqAttr == 'title':
                participantTable.title = request.data[reqAttr] 
            elif reqAttr == 'surname':
                participantTable.surname = request.data[reqAttr]
            elif reqAttr == 'firstname':
                participantTable.firstname = request.data[reqAttr]
            elif reqAttr == 'initials':
                participantTable.initials = request.data[reqAttr] 
            elif reqAttr == 'preferredname':
                participantTable.preferredname = request.data[reqAttr]
            elif reqAttr == 'homelanguage':
                participantTable.homelanguage = request.data[reqAttr]
            elif reqAttr == 'preferredlanguage':
                participantTable.preferredlanguage = request.data[reqAttr]
            elif reqAttr == 'maidenname':
                participantTable.maidenname = request.data[reqAttr]
            elif reqAttr == 'countryofissue':
                participantTable.countryofissue = request.data[reqAttr] 
            elif reqAttr == 'emailaddress':
                participantTable.emailaddress = request.data[reqAttr]
            elif reqAttr == 'usrphonenum':
                participantTable.usrphonenum = request.data[reqAttr]
            elif reqAttr == 'profilepic':
                participantTable.profilepic = request.data[reqAttr]
            elif reqAttr == 'event':

                event = request.data[reqAttr]
                try:
                    eventDetTable = EventDetailTable.objects.get(id = event)  
                    participantTable.events.add(eventDetTable)
                    
                except EventDetailTable.DoesNotExist:
                    return Response("Event does not exists", status=status.HTTP_400_BAD_REQUEST)              
            elif reqAttr == 'user':
                try:
                    usrname = request.data[reqAttr]
                    usr = User.objects.filter(username= request.data[reqAttr]) 
                    if usr.count() == 0 :
                        return Response("User does not exists", status=status.HTTP_400_BAD_REQUEST)
                    participantTable.user = usr
                except ParticipantTable.DoesNotExist:
                    return Response("Something went wrong when retrieving user", status=status.HTTP_409_CONFLICT)
                
        
        print(reqData)
        #participantTable.typefld = request.data['typefld']
        #participantTable.disabled = request.data['disabled']
        #participantTable.gender = request.data['gender']

        #if (hasattr(request.data , 'usrphonenum')) :
        #    participantTable.usrphonenum = request.data['usrphonenum']
        #if (hasattr(request.data , 'profilepic')):
        #    participantTable.profilepic = request.data['profilepic']
        #usr = User.objects.get(id= request.data['user']) ; 
        #participantTable.user = usr
        #   

        participantTable.save() 

        #participantserializer = ParticipantSerializer(participantTable , data=request.data)
        #if participantserializer.is_valid():
        #    participantserializer.save()

        #    return Response("Is valid")       
        #else:
        #    return Response("Is not valid")  
        
        participantserializer = ParticipantSerializer(participantTable , many=False)

        return Response(participantserializer.data , status=status.HTTP_200_OK)   
   
    def partial_update(self , request  , *args, **kwargs):
        participantId = request.data['id']
        participantTable = ParticipantTable.objects.get(id = participantId)        

        participantTable.title = request.data['title']
        #participantTable.surname = request.data['surname']
        #participantTable.firstname = request.data['firstname']
        #participantTable.othernames = request.data['othernames']
        #participantTable.initials = request.data['initials']
        #participantTable.preferredname = request.data['preferredname']
        #participantTable.homelanguage = request.data['homelanguage']
        #participantTable.preferredlanguage = request.data['preferredlanguage']
        #participantTable.maidenname = request.data['maidenname']

        #participantTable.countryofissue = request.data['countryofissue']
        #participantTable.typefld = request.data['typefld']
        #participantTable.disabled = request.data['disabled']
        #participantTable.gender = request.data['gender']
        #participantTable.emailaddress = request.data['emailaddress']

        #participantTable.usrphonenum = request.data['usrphonenum']
        #participantTable.profilepic = request.data['profilepic']
        #participantTable.user = request.data['user']
   
        participantserializer = ParticipantSerializer(participantTable , data=request.data)
        if participantserializer.is_valid():
            #participantserializer.save()
            return Response("In valid")       
        else:
            return Response(participantId)   

        return Response(participantserializer.data)    
 
class participantPaymViewSet(ModelViewSet):
    queryset = ParticipantPaymRefTable.objects.all()
    serializer_class = ParticipantPaymTableSerializer
    parser_classes = (MultiPartParser , FormParser , JSONParser)


    def create(self , request  , *args, **kwargs):

        try:
            participantTable = ParticipantTable.objects.get(id= request.data['participant'])   
        except ParticipantTable.DoesNotExist:
            return Response("Participant not found", status=status.HTTP_404_NOT_FOUND)
        
        try:
            eventTable = EventDetailTable.objects.get(id= request.data['event'])   
        except EventDetailTable.DoesNotExist:
            return Response("Event not found", status=status.HTTP_404_NOT_FOUND)
        
        try:
            eventSubTable = EventSubDetailTable.objects.get(id= request.data['subevent'])   
        except EventSubDetailTable.DoesNotExist:
            return Response("Sub event not found", status=status.HTTP_404_NOT_FOUND)

        try:
            with transaction.atomic():
                participantPaymRefTable = ParticipantPaymRefTable.objects.create(
                    participant = participantTable,
                    merchant_id = request.data['merchant_id'],
                    name_first = request.data['name_first'],
                    name_last = request.data['name_last'],
                    email_address = request.data['email_address'],
                    m_paym_id = request.data['m_payment_id'],
                    amount = request.data['amount'],
                    item_name = request.data['item_name'],
                    payment_uuid = request.data['payment_uuid'],
                    payment_timestamp = request.data['payment_timestamp'],
                    payment_status = request.data['payment_status']
                )    

                if request.data['payment_status'] == 'Completed':
                    participantEventTable = ParticipantEventTable.objects.create(
                        participant = participantTable,
                        event = eventTable,
                        subevent = eventSubTable,
                        paymref = participantPaymRefTable
                    )  
            
                participantpaymserializer = ParticipantPaymTableSerializer(participantPaymRefTable , many=False)

        except Exception as e:
            return Response("Error creating payment reference", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return  Response(participantpaymserializer.data , status=status.HTTP_201_CREATED)

        
    
class EventSubViewSet(ModelViewSet):
    queryset = EventSubDetailTable.objects.all()
    serializer_class = EventSubDetailSerializer
    parser_classes = (MultiPartParser , FormParser , JSONParser)

    def retrieve(self , request  , *args, **kwargs):
        eventid = request.data['event']        

        eventsubDetTable = EventSubDetailTable.objects.filter(event = eventid)    

        eventsubserializer = EventSubDetailSerializer(eventsubDetTable , many=True)
        return  Response(eventsubserializer.data, status=status.HTTP_200_OK)
    
    def list(self , request  , *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        eventid = body['event']        

        eventsubDetTable = EventSubDetailTable.objects.filter(event = eventid)    

        eventsubserializer = EventSubDetailSerializer(eventsubDetTable , many=True)
        return  Response(eventsubserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getPayfastConnectionDetails(request):

    usesandbox = config('PAYFAST_USESANDBOX', cast=bool, default = True)
    merchantid = os.getenv('PAYFAST_SANDBOX_MERCHANT_ID') if usesandbox == True else os.getenv('PAYFAST_MERCHANT_ID')
    merchantkey = os.getenv('PAYFAST_SANDBOX_MERCHANT_KEY') if usesandbox == True else os.getenv('PAYFAST_MERCHANT_KEY')
    merchantpassphrase = os.getenv('PAYFAST_SANDBOX_MERCHANT_PASSPHRASE') if usesandbox == True else os.getenv('PAYFAST_MERCHANT_PASSPHRASE')  
    activationscript = str(os.getenv('PAYFAST_SANDBOX_MERCHANT_ACTIVESCRIPT')) if usesandbox == True else str(os.getenv('PAYFAST_MERCHANT_ACTIVESCRIPT')),  
    activationscriptstring = ''.join(activationscript)
    paymmethods = str(os.getenv('PAYFAST_SANDBOX_MERCHANT_PAYMMETHODS')) if usesandbox == True else str(os.getenv('PAYFAST_MERCHANT_PAYMMETHODS')),  

    routes = {
        'merchantid' : merchantid ,
        'merchantkey' : merchantkey ,
        'merchantpassphrase' : merchantpassphrase,     
        'activationscript' : activationscriptstring,
        'usesandbox' : usesandbox ,
        'paymmethods' : paymmethods
    }

    return Response(routes)