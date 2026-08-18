from django.db.models import Q
from django.utils import timezone

from api.models import AthleticOrganisationTable, EventDetailTable, SubscriptionTable
from api.util import EventStatus, SubscriberType, SubscriptionStatus

ACTIVE_EVENT_STATUSES = (
    EventStatus.Created,
    EventStatus.Planning,
    EventStatus.RegistrationOpen,
    EventStatus.RegistrationClosed,
)

ACTIVE_EVENT_STATUS_VALUES = [status.value for status in ACTIVE_EVENT_STATUSES]


def new_event_status_choices():
    return [(status.value, status.name) for status in ACTIVE_EVENT_STATUSES]


def is_allowed_new_event_status(event_status):
    return int(event_status) in ACTIVE_EVENT_STATUS_VALUES


def validate_club_can_create_event(
    athletic_org_id,
    *,
    event_status=None,
    exclude_event_id=None,
    reference_date=None,
):
    """
    Validate that a club athletic organisation may save an active event.

    Returns None when validation passes, otherwise an error message string.

    For new events, omit exclude_event_id. For updates, pass the existing event pk
    so it is not double-counted among active events for the organisation.
    """
    if not athletic_org_id:
        return None

    if event_status is None:
        event_status = EventStatus.Created
    else:
        event_status = int(event_status)

    if event_status not in ACTIVE_EVENT_STATUS_VALUES:
        return None

    club = AthleticOrganisationTable.objects.filter(pk=athletic_org_id).first()
    if club is None:
        return "Selected athletic organisation was not found."

    today = reference_date or timezone.now().date()

    valid_subscriptions = SubscriptionTable.objects.filter(
        athleticorganisation_id=athletic_org_id,
        subscriptionplan__subscribertype=SubscriberType.Organisation,
        subscriptionplan__isactive=True,
        subscriptionstatus__in=(
            SubscriptionStatus.Trial,
            SubscriptionStatus.Active,
        ),
        subscriptionstartdate__lte=today,
    ).filter(
        Q(subscriptionenddate__isnull=True) | Q(subscriptionenddate__gte=today),
    ).select_related('subscriptionplan')

    if not valid_subscriptions.exists():
        return (
            "This club does not have a valid organisation subscription "
            "(trial or active) covering today's date."
        )

    allowed_events = 0
    has_unlimited = False
    for subscription in valid_subscriptions:
        maximum_events = subscription.subscriptionplan.maximumevents
        if maximum_events is None:
            has_unlimited = True
        else:
            allowed_events += maximum_events

    if has_unlimited:
        return None

    active_events = EventDetailTable.objects.filter(
        athleticorganisation_id=athletic_org_id,
        eventstatus__in=ACTIVE_EVENT_STATUS_VALUES,
    )
    if exclude_event_id:
        active_events = active_events.exclude(pk=exclude_event_id)

    active_event_count = active_events.count()
    projected_count = active_event_count + 1
    if projected_count >= allowed_events:
        action_label = "save" if exclude_event_id else "create"
        return (
            f"Cannot {action_label} this event: the club already has {active_event_count} "
            f"other active event(s) and the valid subscription(s) allow fewer than "
            f"{projected_count} (limit: {allowed_events})."
        )

    return None
