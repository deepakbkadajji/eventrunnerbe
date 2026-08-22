from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import EventNotificationTable
from .models import OrganisationNotificationTable
from .models import ParticipantEventTable
from .models import AthleticOrganisationMemberTable
from .util import OrganisationMemberStatus
from eventrunnerbe.notifications.utils import send_push_notification
from eventrunnerbe.notifications.utils import send_organisation_push_notification
from eventrunnerbe.notifications.utils import update_user
from eventrunnerbe.notifications.utils import update_user_athletic_organisation

@receiver(post_save, sender=EventNotificationTable)
def event_notification_handler(sender, instance, created, **kwargs):
    notificationurlcheck = instance.notificationImg

    if created:
        send_push_notification(
            instance.title,
            None,
            instance.message,
            instance.event.id,
            instance.id,
            instance.notificationImg.url if notificationurlcheck else None,
        )


@receiver(post_save, sender=OrganisationNotificationTable)
def organisation_notification_handler(sender, instance, created, **kwargs):
    if created:
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


@receiver(post_save, sender=ParticipantEventTable)
def participant_subscription_handler(sender, instance, created, **kwargs):
    if created:
        update_user(instance.participant.id, instance.event.id)


def _sync_athletic_organisation_member_tag(instance):
    is_member = instance.status == OrganisationMemberStatus.Active
    update_user_athletic_organisation(
        instance.participant_id,
        instance.athleticorganisation_id,
        is_member=is_member,
    )


@receiver(post_save, sender=AthleticOrganisationMemberTable)
def athletic_organisation_member_save_handler(sender, instance, created, **kwargs):
    _sync_athletic_organisation_member_tag(instance)


@receiver(post_delete, sender=AthleticOrganisationMemberTable)
def athletic_organisation_member_delete_handler(sender, instance, **kwargs):
    update_user_athletic_organisation(
        instance.participant_id,
        instance.athleticorganisation_id,
        is_member=False,
    )