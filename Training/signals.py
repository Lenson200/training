from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Trainee

User = get_user_model()

@receiver(post_save, sender=User)
def create_or_update_trainee_profile(sender, instance, created, **kwargs):
    if instance.is_trainee:
        if created:
            Trainee.objects.get_or_create(user=instance)
        else:
            # Update logic if necessary
            instance.trainee_profile.save()
@receiver(post_save, sender=User)
def save_trainee_profile(sender, instance, **kwargs):
    if instance.is_trainee:
        instance.trainee_profile.save()

@receiver(post_save, sender=User)
def update_trainee_email(sender, instance, created, **kwargs):
    if created:
        Trainee.objects.get_or_create(user=instance, email=instance.email)
    else:
        trainee = instance.trainee_profile
        if trainee:
            trainee.email = instance.email
            trainee.save()
# @receiver(post_save, sender=User)
# def update_trainee_staffnumber(sender, instance, created, **kwargs):
#     if created:
#         Trainee.objects.get_or_create(user=instance, staffnumber=instance.staffnumber)
#     else:
#         trainee = instance.trainee_profile
#         if trainee:
#             trainee.staffnumber = instance.staffnumber
#             trainee.save()
# @receiver(post_save, sender=User)
# def create_trainee_profile(sender, instance, created, **kwargs):
#     if created and instance.is_trainee:
#         Trainee.objects.create(user=instance)