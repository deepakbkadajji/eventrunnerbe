from django.contrib import admin

from .models import EventDetailTable
from .models import ParticipantTable
from .models import EventImages
from .models import EventSubDetailTable
from .models import ParticipantPaymRefTable
from .models import ParticipantEventTable

admin.site.register(EventDetailTable)
admin.site.register(ParticipantTable)
admin.site.register(EventImages)
admin.site.register(EventSubDetailTable)
admin.site.register(ParticipantPaymRefTable)
admin.site.register(ParticipantEventTable)