from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import m2m_changed, post_save, post_delete
from django.dispatch import receiver

from .models import Outcome, Achievements, ProfileDetails
from .models import User, Profile, AdministrationChangeLog, Battle, Room, Message, Notification, Game, BattleParticipant, UserState
from .views import get_changes

@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import AdministrationChangeLog
from .utils import get_current_user, get_changes

@receiver(post_save)
def log_model_save(sender, instance, created, **kwargs):
    if sender == AdministrationChangeLog:
        return

    user = get_current_user()
    if not user or not isinstance(user, get_user_model()):
        return

    action = 'create' if created else 'update'
    model_name = ContentType.objects.get_for_model(sender).model
    changes = get_changes(instance) if not created else None

    try:
        AdministrationChangeLog.objects.create(
            user=user,
            action=action,
            model=model_name,
            object_id=instance.pk,
            changes=changes
        )
    except ValueError as e:

        print(f"Error creating AdministrationChangeLog: {e}")

@receiver(post_delete)
def log_model_delete(sender, instance, **kwargs):
    if sender == AdministrationChangeLog:
        return

    user = get_current_user()
    if not user or not isinstance(user, get_user_model()):
        return

    model_name = ContentType.objects.get_for_model(sender).model

    try:
        AdministrationChangeLog.objects.create(
            user=user,
            action='delete',
            model=model_name,
            object_id=instance.pk
        )
    except ValueError as e:

        print(f"Error creating AdministrationChangeLog: {e}")

@receiver(post_save, sender=Outcome)
def update_achievement_counters(sender, instance, **kwargs):
    user = instance.user
    if not user:
        return

    achievements = Achievements.objects.filter(user=user)

    for achievement in achievements:
        achievement.green_counter += instance.green_counter
        achievement.yellow_counter += instance.yellow_counter
        achievement.orange_counter += instance.orange_counter
        achievement.red_counter += instance.red_counter
        achievement.black_counter += instance.black_counter
        achievement.gold_counter += instance.gold_counter
        achievement.redgold_counter += instance.redgold_counter
        achievement.save()

def update_currencies_for_profile(instance):
    currencies = Currency.objects.exclude(pk=instance.currency.pk)
    for currency in currencies:
        ProfileCurrency.objects.get_or_create(profile=instance, currency=currency)

def populate_other_currencies(sender, instance, **kwargs):
    update_currencies_for_profile(instance)

@receiver(post_save, sender=BattleParticipant)
def update_participant_battle(sender, instance, created, **kwargs):
    if created and instance.battle:
        print(f"Participant added to battle {instance.battle}")

from django.contrib.auth.signals import user_logged_out
from .models import SettingsModel

@receiver(user_logged_out)
def set_notifications_off(sender, request, user, **kwargs):
    try:
        settings = SettingsModel.objects.get(user=user)
        if settings.notifications_status == 'ON':
            settings.notifications_status = 'OFF'
            settings.save()
    except SettingsModel.DoesNotExist:
        pass

@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):
    if created:
        SettingsModel.objects.create(
            user=instance,
            username=instance.username,
            email=instance.email if hasattr(instance, 'email') else None
        )

@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    """
    Signal to create notifications for users in a room when a new message is posted.
    """
    if created:
        message = instance
        try:
            room = Room.objects.get(name=message.room)
            members_to_notify = room.members.exclude(id=message.signed_in_user.id)

            for member in members_to_notify:

                if getattr(member, 'current_room', None) != room.name:

                    user_settings = SettingsModel.objects.filter(user=member).first()
                    if user_settings and user_settings.notifications_status == "ON":
                        notification = Notification.objects.create(
                            content_type=ContentType.objects.get_for_model(Message),
                            object_id=message.id,
                            related_object=message,
                            message=f"{message.signed_in_user.username} sent a message in {room.name}: {message.value}"
                        )

                        notification.user.add(member)
                        notification.save()

        except Room.DoesNotExist:
            print(f"Room '{message.room}' does not exist.")

import queue
from .models import InventoryObject

inventory_sse_queue = queue.Queue()

@receiver([post_save, post_delete], sender=InventoryObject)
def inventory_object_changed(sender, instance, **kwargs):
    inventory_sse_queue.put("changed")

@receiver(post_save, sender=Outcome)
def increment_card_counter(sender, instance, created, **kwargs):
    print('started profile card counter')
    if created and instance.user and not getattr(instance, "demonstration", False):
        try:
            profile = instance.user.profiledetails
            profile.cards_counter = (profile.cards_counter or 0) + 1
            profile.save()
            print('profile card counter updated')
        except ProfileDetails.DoesNotExist:
            pass

@receiver(post_save, sender=User)
def create_user_state(sender, instance, created, **kwargs):
    if created:
        UserState.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_state(sender, instance, **kwargs):
    UserState.objects.get_or_create(user=instance)