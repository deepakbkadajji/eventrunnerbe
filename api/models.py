from django.contrib.auth.models import User
from django.db import models
from treebeard.mp_tree import MP_Node
from .util import EventStatus
from .util import Gender
from .util import SponsorCategory
from .util import OrganisationStatus
from .util import OrganisationMemberStatus
from .util import OrganisationMemberRole
from .util import OrganisationType
from .util import SubscriberType
from .util import BillingFrequency
from .util import SubscriptionStatus

from utilities.storage_backends import PrivateMediaStorage
from utilities.storage_backends import PublicMediaStorage


class OrganisationTable(models.Model):
    name = models.CharField(max_length=100)
    contactperson = models.CharField(max_length=100, blank=True, null=True)
    address1 = models.CharField(max_length=100, blank=True, null=True)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    address3 = models.CharField(max_length=100, blank=True, null=True)
    postcode = models.CharField(max_length=10, blank=True, null=True)
    province = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    lat = models.DecimalField(null=True, blank=True, max_digits=17, decimal_places=14)
    lng = models.DecimalField(null=True, blank=True, max_digits=17, decimal_places=14)
    logo = models.ImageField(upload_to='images/organisationLogo/', blank=True, null=True, storage=PrivateMediaStorage())
    banner = models.ImageField(upload_to='images/organisationBanner/', blank=True, null=True, storage=PrivateMediaStorage())
    website = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=OrganisationStatus.choices(), default=OrganisationStatus.Active)
    athleticassociation = models.ForeignKey(
        'AthleticAssociationTable',
        on_delete=models.RESTRICT,
        related_name='organisation_athleticassociation',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name








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
    allowregistration = models.BooleanField(default=False)
    parkinglat = models.DecimalField(null=True, blank=True, max_digits=17, decimal_places=14)
    parkinglng = models.DecimalField(null=True, blank=True, max_digits=17, decimal_places=14)

    organisation = models.ForeignKey(OrganisationTable , on_delete=models.RESTRICT , related_name='event_organisation')
    athleticorganisation = models.ForeignKey(
        'AthleticOrganisationTable',
        on_delete=models.RESTRICT,
        related_name='event_athleticorganisation',
        null=True,
        blank=True,
    )
    athleticscategory = models.ForeignKey(
        'AthleticsCategoryTable',
        on_delete=models.RESTRICT,
        related_name='event_athleticscategory',
        null=True,
        blank=True,
    )
    venuename = models.CharField(max_length=150, blank=True, null=True)
    sanctionstatus = models.CharField(max_length=20, default='UNREGISTERED')
    sanctionreference = models.CharField(max_length=100, blank=True, null=True)
    registrationopendate = models.DateTimeField(blank=True, null=True)
    registrationclosedate = models.DateTimeField(blank=True, null=True)
    maximumparticipants = models.IntegerField(blank=True, null=True)
    isactive = models.BooleanField(default=True)

    

    def __str__(self):
        return self.eventname

    class Meta:
        ordering = ['-updated']

class OrganisationEventTable(models.Model):
    organisation = models.ForeignKey(OrganisationTable, on_delete=models.CASCADE, related_name='organisationevent_organisation')
    event = models.ForeignKey(EventDetailTable, on_delete=models.CASCADE, related_name='organisationevent_event')

    def __str__(self):
        return f'{self.organisation.name} - {self.event.eventname}'

    class Meta:
        unique_together = ('organisation', 'event')

class EventCategoryTable(models.Model):
    categoryname = models.CharField(max_length=50 , null=False , blank=False)
    #categoryImg = models.ImageField(upload_to='images/eventCategoryImg/' , blank=True , null=True, storage=PrivateMediaStorage())

    def __str__(self):
        return self.categoryname


class AthleticsCategoryTable(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name


class AthleticOrganisationTable(MP_Node):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    organisationtype = models.IntegerField(choices=OrganisationType.choices())
    registrationnumber = models.CharField(max_length=50, blank=True, null=True)
    countrycode = models.CharField(max_length=10, blank=True, null=True)
    province = models.CharField(max_length=50, blank=True, null=True)
    postcode = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    physicaladdress = models.TextField(blank=True, null=True)
    contactname = models.CharField(max_length=50, blank=True, null=True)
    contactsurname = models.CharField(max_length=50, blank=True, null=True)
    contactemail = models.CharField(max_length=100, blank=True, null=True)
    contactphone = models.CharField(max_length=50, blank=True, null=True)
    websiteurl = models.CharField(max_length=255, blank=True, null=True)
    isverified = models.BooleanField(default=False)
    isactive = models.BooleanField(default=True)
    lat = models.DecimalField(null=True, blank=True, max_digits=17, decimal_places=14)
    lng = models.DecimalField(null=True, blank=True, max_digits=17, decimal_places=14)
    created = models.DateTimeField(auto_now_add=True)
    logo = models.ImageField(upload_to='images/AthelicOrgLogo/', blank=True, null=True, storage=PrivateMediaStorage())
    banner = models.ImageField(upload_to='images/AthleticOrgBanner/', blank=True, null=True, storage=PrivateMediaStorage())

    node_order_by = ['name']

    def __str__(self):
        return self.name


class AthleticOrganisationMemberTable(models.Model):
    participant = models.ForeignKey(
        'ParticipantTable',
        on_delete=models.CASCADE,
        related_name='athleticorganisationmember_participant',
    )
    athleticorganisation = models.ForeignKey(
        AthleticOrganisationTable,
        on_delete=models.CASCADE,
        related_name='athleticorganisationmember_athleticorganisation',
    )
    membershipnumber = models.CharField(max_length=50, blank=True, null=True)
    membershiptype = models.CharField(max_length=50, blank=True, null=True)
    role = models.IntegerField(
        choices=OrganisationMemberRole.choices(),
        default=OrganisationMemberRole.Member,
    )
    status = models.IntegerField(
        choices=OrganisationMemberStatus.choices(),
        default=OrganisationMemberStatus.Pending,
    )
    membershipstartdate = models.DateField(blank=True, null=True)
    membershipenddate = models.DateField(blank=True, null=True)
    isprimary = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.athleticorganisation.name} - {self.participant.surname}'

    class Meta:
        unique_together = ('participant', 'athleticorganisation')
        ordering = ['-created']


class AthleticOrganisationCategoryTable(models.Model):
    athleticscategory = models.ForeignKey(
        AthleticsCategoryTable,
        on_delete=models.RESTRICT,
        related_name='athleticorganisationcategory_athleticscategory',
    )
    athleticorganisation = models.ForeignKey(
        AthleticOrganisationTable,
        on_delete=models.CASCADE,
        related_name='athleticorganisationcategory_athleticorganisation',
    )
    isprimary = models.BooleanField(default=False)
    isactive = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.athleticorganisation.name} - {self.athleticscategory.name}'

    class Meta:
        unique_together = ('athleticscategory', 'athleticorganisation')


class AthleticAssociationTable(MP_Node):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    registrationnumber = models.CharField(max_length=50, blank=True, null=True)
    athleticscategory = models.ForeignKey(
        AthleticsCategoryTable,
        on_delete=models.RESTRICT,
        related_name='athleticassociation_athleticscategory',
    )

    node_order_by = ['name']

    def save(self, *args, **kwargs):
        parent = self.get_parent()
        if parent is not None:
            self.athleticscategory = parent.athleticscategory
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class EventSubDetailTable(models.Model):
    name = models.CharField(max_length=50)
    event = models.ForeignKey(EventDetailTable , on_delete=models.CASCADE , related_name='subevent_event')
    eventcategory = models.ForeignKey(EventCategoryTable , on_delete=models.CASCADE , related_name='subevent_eventcategory')
    eventsubdate = models.DateField()
    regfees = models.DecimalField(max_digits=10, decimal_places=2)
    regfeescurrency = models.CharField(max_length=10)
    displaysequence = models.IntegerField(default=0)
    elevationImg = models.ImageField(upload_to='images/subeventsElevationImg/' , blank=True , null=True, storage=PrivateMediaStorage())
    distancevalue = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    distanceunit = models.CharField(max_length=10, blank=True, null=True)
    minimumage = models.IntegerField(blank=True, null=True)
    maximumparticipants = models.IntegerField(blank=True, null=True)
    isactive = models.BooleanField(default=True)

    def __str__(self):
        return self.event.eventname + ' ' + self.name 

class EventInformationTable(models.Model):
    name = models.CharField(max_length=20)
    event = models.ForeignKey(EventDetailTable , on_delete=models.CASCADE , related_name='eventinfo_event')
    infoImg = models.ImageField(upload_to='images/eventInformationImg/' , blank=True , null=True, storage=PrivateMediaStorage())

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
    authid = models.CharField(max_length=50, blank=False, null=False , unique=False)
    identitynumber = models.CharField(max_length=30, blank=True, null=True)
    passportnumber = models.CharField(max_length=30, blank=True, null=True)
    nationalitycode = models.CharField(max_length=3, blank=True, null=True)
    emergencycontactname = models.CharField(max_length=150, blank=True, null=True)
    emergencycontactphone = models.CharField(max_length=50, blank=True, null=True)
    isverified = models.BooleanField(default=False)
    isactive = models.BooleanField(default=True)

    def __str__(self):
        return self.firstname + ' ' + self.surname
    
class OrganisationMemberTable(models.Model):
    organisation = models.ForeignKey(OrganisationTable, on_delete=models.CASCADE, related_name='organisationmember_organisation')
    participant = models.ForeignKey(ParticipantTable, on_delete=models.CASCADE, related_name='organisationmember_participant')
    status = models.IntegerField(choices=OrganisationMemberStatus.choices(), default=OrganisationMemberStatus.Pending)
    role = models.IntegerField(choices=OrganisationMemberRole.choices(), default=OrganisationMemberRole.Member)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.organisation.name} - {self.participant.surname}'

    class Meta:
        unique_together = ('organisation', 'participant')
        ordering = ['-created']

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
    paymref = models.ForeignKey(ParticipantPaymRefTable , on_delete=models.DO_NOTHING , related_name='participantevent_paymref' , null=True , blank=True)  
    participantstatus = models.CharField(max_length=50 , null=True , blank=True)
    eventregdate = models.DateTimeField(max_length=50 , null=True , blank=True)
    bibnumber = models.CharField(max_length=30, blank=True, null=True)
    registrationnumber = models.CharField(max_length=50, blank=True, null=True)
    registrationdate = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.participant.surname + ' ' + self.event.eventname
    

#Event Notification table
class EventNotificationTable(models.Model):
    event = models.ForeignKey(EventDetailTable, on_delete=models.CASCADE  , related_name='eventnotification_event') 
    title = models.CharField(max_length=50 , null=True , blank=True)
    message = models.CharField(max_length=255 , null=True , blank=True)
    notificationImg = models.ImageField(upload_to='images/notificationImg/' , blank=True , null=True, storage=PrivateMediaStorage())
    notificationPdf = models.FileField(upload_to='files/notificationPdf/', blank=True, null=True, storage=PrivateMediaStorage())
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event.eventname + ' ' + self.title

    class Meta:
        ordering = ['-created']

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


class SubscriptionPlanTable(models.Model):
    plancode = models.CharField(max_length=30, unique=True)
    planname = models.CharField(max_length=100)
    subscribertype = models.IntegerField(choices=SubscriberType.choices())
    billingfrequency = models.IntegerField(choices=BillingFrequency.choices())
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currencycode = models.CharField(max_length=3, default='ZAR')
    maximummembers = models.IntegerField(blank=True, null=True)
    maximumevents = models.IntegerField(blank=True, null=True)
    isactive = models.BooleanField(default=True)

    def __str__(self):
        return self.planname


class SubscriptionTable(models.Model):
    subscriptionplan = models.ForeignKey(
        SubscriptionPlanTable,
        on_delete=models.RESTRICT,
        related_name='subscription_plan',
    )
    participant = models.ForeignKey(
        ParticipantTable,
        on_delete=models.CASCADE,
        related_name='subscription_participant',
        blank=True,
        null=True,
    )
    athleticorganisation = models.ForeignKey(
        AthleticOrganisationTable,
        on_delete=models.CASCADE,
        related_name='subscription_athleticorganisation',
        blank=True,
        null=True,
    )
    subscriptionstartdate = models.DateField()
    subscriptionenddate = models.DateField(blank=True, null=True)
    nextbillingdate = models.DateField(blank=True, null=True)
    subscriptionstatus = models.IntegerField(
        choices=SubscriptionStatus.choices(),
        default=SubscriptionStatus.Pending,
    )
    autorenew = models.BooleanField(default=False)
    externalcustomerid = models.CharField(max_length=100, blank=True, null=True)
    externalpaymentid = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        if self.participant:
            return f'{self.subscriptionplan.planname} - {self.participant}'
        if self.athleticorganisation:
            return f'{self.subscriptionplan.planname} - {self.athleticorganisation.name}'
        return self.subscriptionplan.planname


class ErrorTable(models.Model):
    source = models.CharField(max_length=100, blank=True, null=True)
    devicetype = models.CharField(max_length=100, blank=True, null=True)
    app_version = models.CharField(max_length=20, blank=True, null=True)
    app_build = models.CharField(max_length=50, blank=True, null=True)
    app_environment = models.CharField(max_length=50, blank=True, null=True)
    app_version_label = models.CharField(max_length=100, blank=True, null=True)
    error_location = models.CharField(max_length=255, blank=True, null=True)
    error_method = models.CharField(max_length=50, blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    call_stack = models.TextField(blank=True, null=True)
    http_url = models.CharField(max_length=500, blank=True, null=True)
    http_status = models.IntegerField(blank=True, null=True)
    http_call_req_body = models.TextField(blank=True, null=True)
    input_from_user = models.TextField(blank=True, null=True)
    participant = models.ForeignKey(
        ParticipantTable,
        on_delete=models.SET_NULL,
        related_name='error_participant',
        blank=True,
        null=True,
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.source or "error"} - {self.error_location or self.id}'

    class Meta:
        ordering = ['-created']


class AppReleaseVersionTable(models.Model):
    releaseVersionNumber = models.CharField(max_length=50, unique=True)
    optionUpgradeVersionNumber = models.CharField(max_length=50, blank=True, null=True)
    mandatoryUpgradeVersionNumber = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.releaseVersionNumber

    class Meta:
        ordering = ['-created']


class TermsAndConditionsTable(models.Model):
    document_type = models.CharField(max_length=50, default='app')
    version_number = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    content = models.TextField()
    effective_from = models.DateTimeField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.document_type} v{self.version_number}'

    def save(self, *args, **kwargs):
        if self.is_current:
            TermsAndConditionsTable.objects.filter(
                document_type=self.document_type,
                is_current=True,
            ).exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('document_type', 'version_number')
        ordering = ['-created']


class ParticipantTermsAcceptanceTable(models.Model):
    participant = models.ForeignKey(
        ParticipantTable,
        on_delete=models.CASCADE,
        related_name='terms_acceptances',
    )
    terms = models.ForeignKey(
        TermsAndConditionsTable,
        on_delete=models.PROTECT,
        related_name='acceptances',
    )
    accepted_at = models.DateTimeField(auto_now_add=True)
    app_version = models.CharField(max_length=50, blank=True, null=True)
    device_type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.participant} accepted {self.terms}'

    class Meta:
        unique_together = ('participant', 'terms')
        ordering = ['-accepted_at']

