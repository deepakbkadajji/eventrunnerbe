from api.models import AppNotificationTable
from api.models import EventNotificationTable
from api.models import OrganisationNotificationTable

NOTIFICATION_KIND_EVENT = 'event'
NOTIFICATION_KIND_ORGANISATION = 'organisation'
NOTIFICATION_KIND_APP = 'app'

NOTIFICATION_KIND_CHOICES = (
    (NOTIFICATION_KIND_EVENT, 'Event'),
    (NOTIFICATION_KIND_ORGANISATION, 'Organisation'),
    (NOTIFICATION_KIND_APP, 'App'),
)

NOTIFICATION_MODEL_BY_KIND = {
    NOTIFICATION_KIND_EVENT: EventNotificationTable,
    NOTIFICATION_KIND_ORGANISATION: OrganisationNotificationTable,
    NOTIFICATION_KIND_APP: AppNotificationTable,
}


def normalize_notification_kind(value):
    if not isinstance(value, str):
        return None
    kind = value.strip().lower()
    if kind in NOTIFICATION_MODEL_BY_KIND:
        return kind
    return None


def notification_exists(kind, notification_id):
    model = NOTIFICATION_MODEL_BY_KIND.get(kind)
    if model is None:
        return False
    return model.objects.filter(pk=notification_id).exists()


def read_map_for_participant(participant_id, notification_kind=None):
    from api.models import ParticipantNotificationReadTable

    queryset = ParticipantNotificationReadTable.objects.filter(participant_id=participant_id)
    if notification_kind:
        queryset = queryset.filter(notification_kind=notification_kind)
    return {
        (row.notification_kind, row.notification_id): row.read_at
        for row in queryset
    }


def _active_member_organisation_ids(participant_id):
    from api.models import AthleticOrganisationMemberTable
    from api.util import OrganisationMemberStatus

    return AthleticOrganisationMemberTable.objects.filter(
        participant_id=participant_id,
        status=OrganisationMemberStatus.Active,
    ).values_list('athleticorganisation_id', flat=True)


def _event_notifications_for_participant_queryset(participant_id):
    """Event notifications for events the participant is registered for and that are still active."""
    from api.models import ParticipantEventTable
    from api.util import EventStatus

    enrolled_event_ids = ParticipantEventTable.objects.filter(
        participant_id=participant_id,
    ).values_list('event_id', flat=True)
    return EventNotificationTable.objects.filter(
        event_id__in=enrolled_event_ids,
    ).exclude(
        event__eventstatus__in=[EventStatus.Completed, EventStatus.Closed],
    ).select_related('event')


def organisation_notifications_queryset(participant_id):
    from django.db.models import Q

    from api.util import OrganisationNotificationAudience

    member_org_ids = _active_member_organisation_ids(participant_id)
    return OrganisationNotificationTable.objects.filter(
        Q(notification_audience=OrganisationNotificationAudience.Everyone)
        | Q(
            notification_audience=OrganisationNotificationAudience.OrganisationMembersOnly,
            athleticorganisation_id__in=member_org_ids,
        )
    ).select_related('athleticorganisation')


def _media_url(file_field):
    if file_field:
        return file_field.url
    return None


def _inbox_item_from_notification(notification_kind, notification, read_map):
    read_at = read_map.get((notification_kind, notification.id))
    item = {
        'notification_kind': notification_kind,
        'id': notification.id,
        'title': notification.title,
        'message': notification.message,
        'notificationImg': _media_url(notification.notificationImg),
        'notificationPdf': None,
        'club_name': None,
        'event_name': None,
        'is_read': read_at is not None,
        'read_at': read_at.isoformat() if read_at else None,
        'created': notification.created.isoformat(),
    }
    if notification_kind == NOTIFICATION_KIND_EVENT:
        item['notificationPdf'] = _media_url(notification.notificationPdf)
        if getattr(notification, 'event', None):
            item['event_name'] = notification.event.eventname
    elif notification_kind == NOTIFICATION_KIND_ORGANISATION:
        if getattr(notification, 'athleticorganisation', None):
            item['club_name'] = notification.athleticorganisation.name
    return item


def inbox_notifications_for_participant(participant_id, notification_kind=None):
    read_map = read_map_for_participant(participant_id)
    items = []
    kinds = [notification_kind] if notification_kind else list(NOTIFICATION_MODEL_BY_KIND.keys())

    if NOTIFICATION_KIND_APP in kinds:
        for notification in AppNotificationTable.objects.order_by('-created'):
            items.append(_inbox_item_from_notification(NOTIFICATION_KIND_APP, notification, read_map))

    if NOTIFICATION_KIND_EVENT in kinds:
        event_notifications = _event_notifications_for_participant_queryset(
            participant_id,
        ).order_by('-created')
        for notification in event_notifications:
            items.append(_inbox_item_from_notification(NOTIFICATION_KIND_EVENT, notification, read_map))

    if NOTIFICATION_KIND_ORGANISATION in kinds:
        org_notifications = organisation_notifications_queryset(participant_id).select_related(
            'athleticorganisation',
        ).order_by('-created')
        for notification in org_notifications:
            items.append(
                _inbox_item_from_notification(NOTIFICATION_KIND_ORGANISATION, notification, read_map),
            )

    items.sort(key=lambda row: row['created'], reverse=True)
    return items


def unread_event_notification_count(participant_id, event_id):
    from api.models import ParticipantNotificationReadTable
    from api.models import ParticipantTable

    if not ParticipantTable.objects.filter(pk=participant_id).exists():
        return 0

    read_ids = ParticipantNotificationReadTable.objects.filter(
        participant_id=participant_id,
        notification_kind=NOTIFICATION_KIND_EVENT,
    ).values_list('notification_id', flat=True)
    return _event_notifications_for_participant_queryset(participant_id).filter(
        event_id=event_id,
    ).exclude(id__in=read_ids).count()


def event_notification_list_for_participant(participant_id, event_id):
    from api.models import ParticipantTable

    if not ParticipantTable.objects.filter(pk=participant_id).exists():
        return []

    read_map = read_map_for_participant(participant_id, NOTIFICATION_KIND_EVENT)
    notifications = _event_notifications_for_participant_queryset(participant_id).filter(
        event_id=event_id,
    ).order_by('-created')
    return [
        _inbox_item_from_notification(NOTIFICATION_KIND_EVENT, notification, read_map)
        for notification in notifications
    ]


def serializer_context_with_read_status(body, notification_kind):
    participant_id = body.get('participantid')
    if not participant_id:
        return {}
    return {
        'notification_kind': notification_kind,
        'notification_read_map': read_map_for_participant(participant_id, notification_kind),
    }


def unread_counts_for_participant(participant_id):
    from api.models import ParticipantNotificationReadTable

    reads = ParticipantNotificationReadTable.objects.filter(participant_id=participant_id)

    read_app_ids = reads.filter(
        notification_kind=NOTIFICATION_KIND_APP,
    ).values_list('notification_id', flat=True)
    app_unread = AppNotificationTable.objects.exclude(id__in=read_app_ids).count()

    read_event_ids = reads.filter(
        notification_kind=NOTIFICATION_KIND_EVENT,
    ).values_list('notification_id', flat=True)
    event_unread = _event_notifications_for_participant_queryset(participant_id).exclude(
        id__in=read_event_ids,
    ).count()

    read_org_ids = reads.filter(
        notification_kind=NOTIFICATION_KIND_ORGANISATION,
    ).values_list('notification_id', flat=True)
    org_unread = organisation_notifications_queryset(participant_id).exclude(
        id__in=read_org_ids,
    ).count()

    by_kind = {
        NOTIFICATION_KIND_APP: app_unread,
        NOTIFICATION_KIND_ORGANISATION: org_unread,
        NOTIFICATION_KIND_EVENT: event_unread,
    }
    return sum(by_kind.values()), by_kind
