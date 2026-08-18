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
from .models import EventInformationTable
from .models import OrganisationTable
from .models import OrganisationMemberTable
from .models import OrganisationEventTable
from .models import AthleticOrganisationTable
from .models import AthleticOrganisationMemberTable
from .models import AthleticOrganisationCategoryTable
from .models import SubscriptionPlanTable
from .models import SubscriptionTable
from .models import ErrorTable
from .models import AppReleaseVersionTable
from .models import TermsAndConditionsTable
from .models import ParticipantTermsAcceptanceTable
from .models import User
from .util import OrganisationMemberStatus
from .util import OrganisationType
from .util import SubscriberType
from .util import BillingFrequency
from .util import SubscriptionStatus

class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImages
        #fields = '__all__'
        fields = ['id' , 'event_id' , 'eventMainImg']

class EventSubDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='eventcategory.categoryname')

    class Meta:
        model = EventSubDetailTable
        fields = [
            'id', 'event', 'name', 'eventcategory', 'category_name', 'eventsubdate',
            'regfees', 'regfeescurrency', 'displaysequence', 'elevationImg',
            'distancevalue', 'distanceunit', 'minimumage', 'maximumparticipants', 'isactive',
        ]


class ParticipantRegisteredSubeventSerializer(EventSubDetailSerializer):
    registered = serializers.SerializerMethodField()

    class Meta(EventSubDetailSerializer.Meta):
        fields = EventSubDetailSerializer.Meta.fields + ['registered']

    def get_registered(self, obj):
        registered_ids = self.context.get('registered_subevent_ids', set())
        return obj.id in registered_ids

class EventNotificationSerializer(serializers.ModelSerializer):

    event_name = serializers.ReadOnlyField(source='event.eventname')

    class Meta:
        model = EventNotificationTable
        fields = [
            'id', 'event', 'title', 'message', 'notificationImg', 'notificationPdf',
            'event_name', 'created',
        ]
        read_only_fields = ['created']

class EventSponsorSerializer(serializers.ModelSerializer):
    event_name = serializers.ReadOnlyField(source='event.eventname')

    class Meta:
        model = EventSponsorTable
        fields = ['id' , 'event' , 'companyname' , 'description' , 'sponsorImg' , 'externallink' , 'event_name', 'sponsorcategory']

class EventListSerializer(serializers.ModelSerializer):
    eventstatus_label = serializers.CharField(source='get_eventstatus_display', read_only=True)

    class Meta:
        model = EventDetailTable
        fields = [
            'id', 'eventname', 'eventdate', 'eventenddate', 'eventstatus',
            'eventstatus_label', 'eventtype', 'contactpersonname', 'contactpersonemailaddr',
            'venuename', 'sanctionstatus', 'isactive',
        ]


class EventCardSerializer(serializers.ModelSerializer):
    eventimage = EventImageSerializer(source='eventimage_event', many=False, read_only=True)
    athleticscategory_name = serializers.ReadOnlyField(source='athleticscategory.name')
    athleticorganisation_name = serializers.ReadOnlyField(source='athleticorganisation.name')

    class Meta:
        model = EventDetailTable
        fields = [
            'id', 'eventname', 'eventdate', 'eventenddate', 'eventimage',
            'athleticscategory_name', 'athleticorganisation_name', 'eventstatus',
        ]


class EventDetailSerializer(serializers.ModelSerializer):
    #eventimgs = EventImageSerializer(many=False , read_only=True)
    #subeventsvar = EventSubDetailSerializer(source = 'EventSubDetailTable_set' , many=True , read_only=True )
    subevents = EventSubDetailSerializer(source = 'subevent_event' , many=True , read_only=True )
    eventimage = EventImageSerializer(source = 'eventimage_event' , many=False , read_only=True )
    eventnotifications = serializers.SerializerMethodField()
    eventsponsors = EventSponsorSerializer(source = 'eventsponsor_event' , many=True , read_only=True )
    organisation_name = serializers.ReadOnlyField(source='organisation.name')
    athleticorganisation_name = serializers.ReadOnlyField(source='athleticorganisation.name')
    athleticscategory_name = serializers.ReadOnlyField(source='athleticscategory.name')

    def get_eventnotifications(self, obj):
        notifications = sorted(
            obj.eventnotification_event.all(),
            key=lambda notification: notification.created,
            reverse=True,
        )
        return EventNotificationSerializer(notifications, many=True).data

    class Meta:
        model = EventDetailTable
        #fields = '__all__'
        #field = ['id' , 'eventid' , 'eventname' , 'updated' , 'created' ]
        #,'eventimgs' , 'eventid'
        fields = [
            'id', 'eventid', 'eventname', 'eventdate', 'eventenddate', 'updated', 'created',
            'contactpersonname', 'contactpersonsurname', 'contactpersonothername',
            'contactpersonemailaddr', 'contactpersonphonenum', 'eventstatus',
            'contactpersoncitizenship', 'contactpersonnationality', 'contactpersonprovince',
            'contactpersoncountry', 'contactpersonaddrtype', 'contactpersonaddr1',
            'contactpersonaddr2', 'contactpersonaddr3', 'contactpersonaddr4',
            'contactpersonaddrcode', 'terminationstatus', 'eventdescription', 'eventtype',
            'eventcategory', 'startPointLat', 'startPointLng', 'allowregistration',
            'parkinglat', 'parkinglng', 'organisation', 'organisation_name',
            'athleticorganisation', 'athleticorganisation_name', 'athleticscategory',
            'athleticscategory_name', 'venuename', 'sanctionstatus', 'sanctionreference',
            'registrationopendate', 'registrationclosedate', 'maximumparticipants', 'isactive',
            'subevents', 'eventimage', 'eventnotifications', 'eventsponsors',
        ]


class ParticipantRegisteredEventSerializer(EventDetailSerializer):
    subevents = serializers.SerializerMethodField()
    subevent_ids = serializers.SerializerMethodField()

    class Meta(EventDetailSerializer.Meta):
        fields = EventDetailSerializer.Meta.fields + ['subevent_ids']

    def get_subevent_ids(self, obj):
        return self.context.get('subevents_by_event', {}).get(obj.id, [])

    def get_subevents(self, obj):
        registered_ids = set(self.context.get('subevents_by_event', {}).get(obj.id, []))
        return ParticipantRegisteredSubeventSerializer(
            obj.subevent_event.all(),
            many=True,
            context={'registered_subevent_ids': registered_ids},
        ).data

class EventInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventInformationTable
        fields = '__all__'

class ParticipantSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        model = ParticipantTable
        fields = '__all__'


class ParticipantDetailSerializer(ParticipantSerializer):
    organisations = serializers.SerializerMethodField()

    def get_organisations(self, obj):
        organisations = [
            membership.athleticorganisation
            for membership in obj.athleticorganisationmember_participant.filter(
                status=OrganisationMemberStatus.Active,
            )
        ]
        return AthleticOrganisationSerializer(organisations, many=True).data

class ParticipantPaymTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantPaymRefTable
        fields = '__all__'

class ParticipantEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantEventTable
        fields = [
            'id', 'participant', 'event', 'subevent', 'paymref', 'participantstatus',
            'eventregdate', 'bibnumber', 'registrationnumber', 'registrationdate', 'created',
        ]



class AppSponsorSerializer(serializers.ModelSerializer):
    event_name = serializers.ReadOnlyField(source='event.eventname')

    class Meta:
        model = AppSponsorTable
        fields = ['id' , 'companyname' , 'description' , 'sponsorImg' , 'externallink' , 'event_name', 'sponsorcategory']


class OrganisationMemberSerializer(serializers.ModelSerializer):
    organisation_name = serializers.ReadOnlyField(source='organisation.name')
    participant_name = serializers.SerializerMethodField()

    def get_participant_name(self, obj):
        return f'{obj.participant.firstname or ""} {obj.participant.surname or ""}'.strip()

    class Meta:
        model = OrganisationMemberTable
        fields = ['id', 'organisation', 'participant', 'status', 'role', 'created', 'organisation_name', 'participant_name']


class OrganisationEventSerializer(serializers.ModelSerializer):
    organisation_name = serializers.ReadOnlyField(source='organisation.name')
    event_name = serializers.ReadOnlyField(source='event.eventname')

    class Meta:
        model = OrganisationEventTable
        fields = ['id', 'organisation', 'event', 'organisation_name', 'event_name']


class OrganisationSerializer(serializers.ModelSerializer):
    organisationmembers = OrganisationMemberSerializer(source='organisationmember_organisation', many=True, read_only=True)
    organisationevents = OrganisationEventSerializer(source='organisationevent_organisation', many=True, read_only=True)

    class Meta:
        model = OrganisationTable
        fields = [
            'id', 'name', 'contactperson', 'address1', 'address2', 'address3',
            'postcode', 'province', 'country', 'lat', 'lng', 'logo', 'banner',
            'website', 'email', 'phone', 'created', 'status', 'organisationmembers', 'organisationevents',
        ]


class AthleticOrganisationSerializer(serializers.ModelSerializer):
    organisationtype_name = serializers.SerializerMethodField()
    parent_id = serializers.SerializerMethodField()

    def get_organisationtype_name(self, obj):
        try:
            return OrganisationType(obj.organisationtype).name
        except ValueError:
            return None

    def get_parent_id(self, obj):
        parent = obj.get_parent()
        return parent.id if parent else None

    class Meta:
        model = AthleticOrganisationTable
        fields = [
            'id', 'path', 'depth', 'numchild', 'parent_id',
            'code', 'name', 'organisationtype', 'organisationtype_name',
            'registrationnumber', 'countrycode', 'province', 'postcode', 'city',
            'physicaladdress', 'contactname', 'contactsurname', 'contactemail',
            'contactphone', 'websiteurl', 'isverified', 'isactive',
            'lat', 'lng', 'logo', 'banner', 'created',
        ]


class AthleticOrganisationMemberSerializer(serializers.ModelSerializer):
    athleticorganisation_name = serializers.ReadOnlyField(source='athleticorganisation.name')
    participant_name = serializers.SerializerMethodField()

    def get_participant_name(self, obj):
        return f'{obj.participant.firstname or ""} {obj.participant.surname or ""}'.strip()

    class Meta:
        model = AthleticOrganisationMemberTable
        fields = [
            'id', 'participant', 'participant_name', 'athleticorganisation', 'athleticorganisation_name',
            'membershipnumber', 'membershiptype', 'role', 'status',
            'membershipstartdate', 'membershipenddate', 'isprimary', 'created',
        ]


class AthleticOrganisationCategorySerializer(serializers.ModelSerializer):
    athleticorganisation_name = serializers.ReadOnlyField(source='athleticorganisation.name')
    athleticscategory_name = serializers.ReadOnlyField(source='athleticscategory.name')

    class Meta:
        model = AthleticOrganisationCategoryTable
        fields = [
            'id', 'athleticscategory', 'athleticscategory_name',
            'athleticorganisation', 'athleticorganisation_name',
            'isprimary', 'isactive',
        ]


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    subscribertype_name = serializers.SerializerMethodField()
    billingfrequency_name = serializers.SerializerMethodField()

    def get_subscribertype_name(self, obj):
        try:
            return SubscriberType(obj.subscribertype).name
        except ValueError:
            return None

    def get_billingfrequency_name(self, obj):
        try:
            return BillingFrequency(obj.billingfrequency).name
        except ValueError:
            return None

    class Meta:
        model = SubscriptionPlanTable
        fields = [
            'id', 'plancode', 'planname', 'subscribertype', 'subscribertype_name',
            'billingfrequency', 'billingfrequency_name', 'price', 'currencycode',
            'maximummembers', 'maximumevents', 'isactive',
        ]


class SubscriptionSerializer(serializers.ModelSerializer):
    subscriptionplan_name = serializers.ReadOnlyField(source='subscriptionplan.planname')
    subscriptionplan_code = serializers.ReadOnlyField(source='subscriptionplan.plancode')
    participant_name = serializers.SerializerMethodField()
    athleticorganisation_name = serializers.ReadOnlyField(source='athleticorganisation.name')
    subscriptionstatus_name = serializers.SerializerMethodField()

    def get_participant_name(self, obj):
        if not obj.participant:
            return None
        return f'{obj.participant.firstname or ""} {obj.participant.surname or ""}'.strip()

    def get_subscriptionstatus_name(self, obj):
        try:
            return SubscriptionStatus(obj.subscriptionstatus).name
        except ValueError:
            return None

    class Meta:
        model = SubscriptionTable
        fields = [
            'id', 'subscriptionplan', 'subscriptionplan_name', 'subscriptionplan_code',
            'participant', 'participant_name', 'athleticorganisation', 'athleticorganisation_name',
            'subscriptionstartdate', 'subscriptionenddate', 'nextbillingdate',
            'subscriptionstatus', 'subscriptionstatus_name', 'autorenew',
            'externalcustomerid', 'externalpaymentid',
        ]


class ErrorSerializer(serializers.ModelSerializer):
    participant_id = serializers.PrimaryKeyRelatedField(
        source='participant',
        queryset=ParticipantTable.objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = ErrorTable
        fields = [
            'id',
            'source',
            'devicetype',
            'app_version',
            'app_build',
            'app_environment',
            'app_version_label',
            'error_location',
            'error_method',
            'error_message',
            'call_stack',
            'http_url',
            'http_status',
            'http_call_req_body',
            'input_from_user',
            'participant_id',
            'created',
        ]
        read_only_fields = ['id', 'created']


class AppReleaseVersionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppReleaseVersionTable
        fields = [
            'id',
            'releaseVersionNumber',
            'optionUpgradeVersionNumber',
            'mandatoryUpgradeVersionNumber',
            'created',
            'updated',
        ]
        read_only_fields = ['id', 'created', 'updated']


class TermsAndConditionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = TermsAndConditionsTable
        fields = [
            'id',
            'document_type',
            'version_number',
            'title',
            'content',
            'effective_from',
            'is_current',
            'created',
        ]
        read_only_fields = ['id', 'created']


class ParticipantTermsAcceptanceSerializer(serializers.ModelSerializer):
    participant_id = serializers.PrimaryKeyRelatedField(
        source='participant',
        queryset=ParticipantTable.objects.all(),
    )
    terms_id = serializers.PrimaryKeyRelatedField(
        source='terms',
        queryset=TermsAndConditionsTable.objects.all(),
    )
    version_number = serializers.ReadOnlyField(source='terms.version_number')
    document_type = serializers.ReadOnlyField(source='terms.document_type')

    class Meta:
        model = ParticipantTermsAcceptanceTable
        fields = [
            'id',
            'participant_id',
            'terms_id',
            'version_number',
            'document_type',
            'accepted_at',
            'app_version',
            'device_type',
        ]
        read_only_fields = ['id', 'accepted_at']


class ParticipantTermsStatusSerializer(serializers.Serializer):
    accepted = serializers.BooleanField()
    document_type = serializers.CharField()
    current_terms_id = serializers.IntegerField(allow_null=True)
    current_version = serializers.CharField(allow_null=True)
    current_terms = TermsAndConditionsSerializer(allow_null=True, required=False)
    last_accepted_terms_id = serializers.IntegerField(allow_null=True)
    last_accepted_version = serializers.CharField(allow_null=True)
    last_accepted_at = serializers.DateTimeField(allow_null=True)

