from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EventNotificationTable
from .models import ParticipantEventTable
from eventrunnerbe.notifications.utils import send_push_notification 
from eventrunnerbe.notifications.utils import update_user    


@receiver(post_save, sender=EventNotificationTable)
def event_notification_handler(sender, instance, created, **kwargs):
    notificationurl = instance.notificationImg.url
    notificationurlcheck = instance.notificationImg

    if created:
        send_push_notification(instance.title , None, instance.message , instance.event.id , instance.id ,  instance.notificationImg.url if notificationurlcheck else None)


@receiver(post_save, sender=ParticipantEventTable)
def participant_subscription_handler(sender, instance, created, **kwargs):
    if created:
        update_user(instance.participant.id, instance.event.id)