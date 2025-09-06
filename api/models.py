from django.contrib.auth.models import User
from django.db import models
from .util import EventStatus
from .util import Gender

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

#Participant table
class ParticipantTable(models.Model):
    user = models.ForeignKey(User , on_delete=models.RESTRICT , related_name='user' , default=3)
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
    emailaddress = models.CharField(max_length=50, null=True, blank=True)
    usrphonenum = models.CharField(max_length=50, null=True, blank=True)
    profilepic = models.ImageField(upload_to='images/profilepic/' , blank=True , null=True)
    events = models.ManyToManyField(EventDetailTable , blank=True, null=True)
    authid = models.CharField(max_length=50, blank=False, null=False , unique=True)

    def __str__(self):
        return self.surname
    

class EventImages(models.Model):
    event = models.OneToOneField(EventDetailTable , related_name = 'event' , on_delete=models.CASCADE)
    eventMainImg = models.ImageField(upload_to='images/eventsmain/' , blank=True , null=True)

    def __str__(self):
        return 'image'
        
#Event Participant table
#class EventParticipantTable(models.Model):
#    participant = models.ForeignKey(ParticipantTable , on_delete=models.CASCADE)
#    eventid = models.ForeignKey(EventDetailTable, on_delete=models.CASCADE)
#    participantstatus = models.CharField(max_length=50 , null=True)
#    eventstatus = models.CharField(max_length=50 , null=True)
#    eventlinkdate = models.DateTimeField(max_length=50)

#    def __str__(self):
#        return self.participantstatus
