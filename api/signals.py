import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import EventNotificationTable
from .models import OrganisationNotificationTable
from .models import AppNotificationTable
from .models import ParticipantEventTable
from .models import AthleticOrganisationMemberTable
from .util import OrganisationMemberStatus
from eventrunnerbe.notifications.utils import send_push_notification
from eventrunnerbe.notifications.utils import send_organisation_push_notification
from eventrunnerbe.notifications.utils import send_app_push_notification
from eventrunnerbe.notifications.utils import update_user
from eventrunnerbe.notifications.utils import update_user_athletic_organisation

logger = logging.getLogger(__name__)


@receiver(post_save, sender=EventNotificationTable)
def event_notification_handler(sender, instance, created, **kwargs):
    if not created:
        return

    try:
        send_push_notification(
            instance.title,
            None,
            instance.message,
            instance.event.id,
            instance.id,
            instance.notificationImg.url if instance.notificationImg else None,
        )
    except Exception:
        logger.exception(
            "Failed to send event push notification",
            extra={"event_id": instance.event_id, "notification_id": instance.id},
        )


@receiver(post_save, sender=OrganisationNotificationTable)
def organisation_notification_handler(sender, instance, created, **kwargs):
    if not created:
        return

    try:
        send_organisation_push_notification(
            instance.title,
            None,
            instance.message,
            instance.athleticorganisation_id,
            instance.id,
            instance.notification_audience,
            event_id=instance.event_id,
            image_url=instance.notificationImg.url if instance.notificationImg else None,
        )
    except Exception:
        logger.exception(
            "Failed to send organisation push notification",
            extra={
                "athleticorganisation_id": instance.athleticorganisation_id,
                "notification_id": instance.id,
                "event_id": instance.event_id,
            },
        )


@receiver(post_save, sender=AppNotificationTable)
def app_notification_handler(sender, instance, created, **kwargs):
    if not created:
        return

    try:
        send_app_push_notification(
            instance.title,
            None,
            instance.message,
            instance.id,
            instance.notificationImg.url if instance.notificationImg else None,
        )
    except Exception:
        logger.exception(
            "Failed to send app push notification",
            extra={"notification_id": instance.id},
        )


@receiver(post_save, sender=ParticipantEventTable)
def participant_subscription_handler(sender, instance, created, **kwargs):
    if not created:
        return

    try:
        update_user(instance.participant.id, instance.event.id)
    except Exception:
        logger.exception(
            "Failed to update OneSignal user event tag",
            extra={
                "participant_id": instance.participant_id,
                "event_id": instance.event_id,
            },
        )


def _sync_athletic_organisation_member_tag(instance):
    is_member = instance.status == OrganisationMemberStatus.Active
    update_user_athletic_organisation(
        instance.participant_id,
        instance.athleticorganisation_id,
        is_member=is_member,
    )


@receiver(post_save, sender=AthleticOrganisationMemberTable)
def athletic_organisation_member_save_handler(sender, instance, created, **kwargs):
    try:
        _sync_athletic_organisation_member_tag(instance)
    except Exception:
        logger.exception(
            "Failed to sync athletic organisation member OneSignal tag",
            extra={
                "participant_id": instance.participant_id,
                "athleticorganisation_id": instance.athleticorganisation_id,
                "member_created": created,
            },
        )


@receiver(post_delete, sender=AthleticOrganisationMemberTable)
def athletic_organisation_member_delete_handler(sender, instance, **kwargs):
    try:
        update_user_athletic_organisation(
            instance.participant_id,
            instance.athleticorganisation_id,
            is_member=False,
        )
    except Exception:
        logger.exception(
            "Failed to clear athletic organisation member OneSignal tag",
            extra={
                "participant_id": instance.participant_id,
                "athleticorganisation_id": instance.athleticorganisation_id,
            },
        )
