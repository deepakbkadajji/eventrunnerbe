from django.contrib.auth.models import User
from django.db import models
from .util import EventStatus
from .util import Gender
from .util import SponsorCategory

from utilities.storage_backends import PrivateMediaStorage
from utilities.storage_backends import PublicMediaStorage

# Event table
class EventDetailTable(models.Model):
    eventid = models.CharField(max_length=20)
    eventname = models.CharField(max_length=50)
    eventdate = models.DateField()
    eventenddate = models.DateField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    contactpersonname = models.CharField(max_length=50)
    contactpersonsurname = models.CharField(max_length=50)
    contactpersonothername = models.CharField(max_length=99 , default='' , blank=True , null=True)
    contactpersonemailaddr = models.CharField(max_length=50 , default='', blank=True , null=True)
    contactpersonphonenum = models.CharField(max_length=50 , default='', blank=True , null=True)
    eventstatus = models.IntegerField(choices=EventStatus.choices(), default=EventStatus.Created)
    
    contactpersoncitizenship = models.CharField(max_length=50 , default='', blank=True , null=True)
    contactpersonnationality = models.CharField(max_length=50, default='', blank=True , null=True)

    contactpersonprovince = models.CharField(max_length=50, default='', blank=True , null=True)
    contactpersoncountry = models.CharField(max_length=50, default='', blank=True , null=True)

    contactpersonaddrtype = models.CharField(max_length=50, default='', blank=True , null=True)
    contactpersonaddr1 = models.CharField(max_length=50, default='', blank=True , null=True)
    contactpersonaddr2 = models.CharField(max_length=50, default='', blank=True , null=True)
    contactpersonaddr3 = models.CharField(max_length=50, default='', blank=True , null=True)
    contactpersonaddr4 = models.CharField(max_length=50, default='', blank=True , null=True)
    contactpersonaddrcode = models.CharField(max_length=10, default='', blank=True , null=True)

    terminationstatus = models.CharField(max_length=50, default='', blank=True , null=True)
    eventdescription = models.TextField()
    eventtype = models.CharField(max_length=50)
    eventcategory = models.CharField(max_length=50)
    startPointLat = models.DecimalField(null=True, max_digits=17, decimal_places=14)
    startPointLng = models.DecimalField(null=True, max_digits=17, decimal_places=14)


    def __str__(self):
        return self.eventname

    class Meta:
        ordering = ['-updated']

class EventCategoryTable(models.Model):
    categoryname = models.CharField(max_length=50 , null=False , blank=False)

    def __str__(self):
        return self.categoryname


class EventSubDetailTable(models.Model):
    name = models.CharField(max_length=50)
    event = models.ForeignKey(EventDetailTable , on_delete=models.CASCADE , related_name='subevent_event')
    eventcategory = models.ForeignKey(EventCategoryTable , on_delete=models.CASCADE , related_name='subevent_eventcategory')
    eventsubdate = models.DateField()
    regfees = models.DecimalField(max_digits=10, decimal_places=2)
    regfeescurrency = models.CharField(max_length=10)
    displaysequence = models.IntegerField(default=0)

    def __str__(self):
        return self.event.eventname + ' ' + self.name 


#Participant table
class ParticipantTable(models.Model):
    user = models.ForeignKey(User , on_delete=models.RESTRICT , related_name='user')
    title = models.CharField(max_length=10 , null=True , blank=True)
    surname = models.CharField(max_length=50, blank=True, null=True)
    firstname = models.CharField(max_length=50 , null=True, blank=True)
    othernames = models.CharField(max_length=99 , blank=True, null=True)
    initials = models.CharField(max_length=10, null=True, blank=True)
    preferredname = models.CharField(max_length=50, null=True, blank=True)
    homelanguage = models.CharField(max_length=50, null=True, blank=True)
    preferredlanguage = models.CharField(max_length=50, null=True, blank=True)
    maidenname = models.CharField(max_length=50, null=True, blank=True)
    countryofissue = models.CharField(max_length=50, null=True, blank=True)
    typefld = models.CharField(max_length=50, null=True, blank=True)
    disabled = models.BooleanField(default=False) 
    gender = models.IntegerField(choices=Gender.choices, default=Gender.notDefined)
    dateOfBirth = models.DateField( null=True, blank=True)
    emailaddress = models.CharField(max_length=50, null=False, blank=False , unique=True)
    usrphonenum = models.CharField(max_length=50, null=True, blank=True)
    profilepic = models.ImageField(upload_to='images/profilepic/' , blank=True , null=True , storage=PrivateMediaStorage())
    events = models.ManyToManyField(EventDetailTable , blank=True, null=True)
    authid = models.CharField(max_length=50, blank=False, null=False , unique=True)

    def __str__(self):
        return self.surname
    

class EventImages(models.Model):
    event = models.OneToOneField(EventDetailTable , related_name = 'eventimage_event' , on_delete=models.CASCADE)
    eventMainImg = models.ImageField(upload_to='images/eventsmain/' , blank=True , null=True, storage=PrivateMediaStorage())

    def __str__(self):
        return 'image'       

class ParticipantPaymRefTable(models.Model):
    participant = models.ForeignKey(ParticipantTable , on_delete=models.RESTRICT , related_name='Participant')
    merchant_id = models.CharField(max_length=10 , null=True , blank=True)
    name_first = models.CharField(max_length=50, blank=True, null=True)
    name_last = models.CharField(max_length=50 , null=True, blank=True)
    email_address = models.CharField(max_length=99 , blank=True, null=True)
    m_paym_id = models.CharField(max_length=30, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    item_name = models.CharField(max_length=50, null=True, blank=True)
    payment_uuid = models.CharField(max_length=50, null=True, blank=True)
    payment_timestamp = models.CharField(max_length=30, null=True, blank=True)
    payment_status = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.participant.surname + ' ' + self.m_paym_id
    

#Event Participant table
class ParticipantEventTable(models.Model):
    participant = models.ForeignKey(ParticipantTable , on_delete=models.CASCADE , related_name='participantevent_participant')
    event = models.ForeignKey(EventDetailTable, on_delete=models.CASCADE  , related_name='participantevent_event')
    subevent = models.ForeignKey(EventSubDetailTable , on_delete=models.CASCADE, related_name='participantevent_subevent')  
    paymref = models.ForeignKey(ParticipantPaymRefTable , on_delete=models.DO_NOTHING , related_name='participantevent_paymref')  
    participantstatus = models.CharField(max_length=50 , null=True , blank=True)
    eventregdate = models.DateTimeField(max_length=50 , null=True , blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.participant.surname + ' ' + self.event.eventname
    

#Event Notification table
class EventNotificationTable(models.Model):
    event = models.ForeignKey(EventDetailTable, on_delete=models.CASCADE  , related_name='eventnotification_event') 
    title = models.CharField(max_length=50 , null=True , blank=True)
    message = models.CharField(max_length=255 , null=True , blank=True)
    notificationImg = models.ImageField(upload_to='images/notificationImg/' , blank=True , null=True, storage=PrivateMediaStorage())

    def __str__(self):
        return self.event.eventname + ' ' + self.title
    

class EventSponsorTable(models.Model):
    event = models.ForeignKey(EventDetailTable, on_delete=models.CASCADE  , related_name='eventsponsor_event') 
    companyname = models.CharField(max_length=100 , null=True , blank=True)
    description = models.CharField(max_length=255 , null=True , blank=True)
    sponsorImg = models.ImageField(upload_to='images/eventsponsorImg/' , blank=True , null=True, storage=PrivateMediaStorage())
    externallink = models.CharField(max_length=255 , null=True , blank=True)
    sponsorcategory = models.IntegerField(choices=SponsorCategory.choices(), default=SponsorCategory.notDefined)

    def __str__(self):
        return self.event.eventname + ' ' + self.description
    

class AppSponsorTable(models.Model):
    companyname = models.CharField(max_length=100 , null=True , blank=True)
    description = models.CharField(max_length=255 , null=True , blank=True)
    sponsorImg = models.ImageField(upload_to='images/appsponsorImg/' , blank=True , null=True, storage=PrivateMediaStorage())
    externallink = models.CharField(max_length=255 , null=True , blank=True)
    sponsorcategory = models.IntegerField(choices=SponsorCategory.choices(), default=SponsorCategory.notDefined)

    def __str__(self):
        return self.description
    


