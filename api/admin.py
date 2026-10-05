from django.contrib import admin

from .models import EventDetailTable
from .models import ParticipantTable
from .models import EventImages
from .models import EventSubDetailTable
from .models import ParticipantPaymRefTable
from .models import ParticipantEventTable
from .models import EventNotificationTable
from .models import OrganisationNotificationTable
from .models import AppNotificationTable
from .models import EventCategoryTable
from .models import AthleticsCategoryTable
from .models import AthleticAssociationTable
from .models import EventSponsorTable
from .models import AppSponsorTable
from .models import EventInformationTable
from .models import OrganisationTable
from .models import OrganisationMemberTable
from .models import OrganisationEventTable
from .models import AppReleaseVersionTable
from .models import TermsAndConditionsTable
from .models import ParticipantTermsAcceptanceTable
from .models import ParticipantNotificationReadTable

admin.site.register(EventDetailTable)
admin.site.register(ParticipantTable)
admin.site.register(EventImages)
admin.site.register(EventSubDetailTable)
admin.site.register(ParticipantPaymRefTable)
admin.site.register(ParticipantEventTable)
admin.site.register(EventNotificationTable)
admin.site.register(OrganisationNotificationTable)
admin.site.register(AppNotificationTable)
admin.site.register(EventCategoryTable)
admin.site.register(AthleticsCategoryTable)
admin.site.register(AthleticAssociationTable)
admin.site.register(EventSponsorTable)
admin.site.register(AppSponsorTable)
admin.site.register(EventInformationTable)
admin.site.register(OrganisationTable)
admin.site.register(OrganisationMemberTable)
admin.site.register(OrganisationEventTable)
admin.site.register(AppReleaseVersionTable)
admin.site.register(TermsAndConditionsTable)
admin.site.register(ParticipantTermsAcceptanceTable)
admin.site.register(ParticipantNotificationReadTable)
