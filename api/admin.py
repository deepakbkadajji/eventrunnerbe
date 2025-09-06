from django.contrib import admin

from .models import EventDetailTable
from .models import ParticipantTable
from .models import EventImages


admin.site.register(EventDetailTable)
admin.site.register(ParticipantTable)
admin.site.register(EventImages)