from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from rest_framework.authtoken.models import Token    # [Token Model]
from .models import (User, Profile)
########################################################### [1] User Model Signal ###################################################

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Creates or updates the Profile instance linked to the User.
    """
    def create_profile():
        Profile.objects.update_or_create(
            user=instance,
            defaults={
                'age': instance.age,
                'gender': instance.gender,
                'chronic_disease': instance.chronic_disease,
                'phone': instance.phone,
            }
        )
    # Ensure this is done only after the transaction has been committed
    if created:
        transaction.on_commit(create_profile)
    else:
        create_profile()
        
########################################################### [2] Token Signal ########################################################

@receiver(post_save, sender=User)
def Token_Create_Automation(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)

########################################################### [3] Patient Profile Signal ##############################################

def create_or_update_user_profile(sender, instance, created, **kwargs):
    # Create profile if it doesn't exist
    if created:
        Profile.objects.create(user=instance)
    else:
        # Update profile if it exists
        if hasattr(instance, 'profile'):
            instance.profile.first_name = instance.first_name
            instance.profile.last_name = instance.last_name
            instance.profile.phone = instance.phone  # Update phone
            instance.profile.age = instance.age
            instance.profile.gender = instance.gender
            instance.profile.chronic_disease = instance.chronic_disease
            instance.profile.save()
            