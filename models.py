from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token    # [Token Model]
from django.conf import settings
from django.db import transaction
from django.core.validators import RegexValidator

##################################################################################################################

class UserManager(BaseUserManager):
    def create_user(self, email, full_name=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("User must have an email address !")
        if not password:
            raise ValueError("Users must have a password !")
        if not full_name:
            raise ValueError("Users must have a fullname !")
        
        user_obj = self.model(
            email=self.normalize_email(email),
            full_name = full_name,
        )
        user_obj.active = is_active
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, full_name=None, password=None):
        return self.create_user(email, full_name=full_name, password=password, is_staff=True)

    def create_superuser(self, email, full_name=None, password=None):
        return self.create_user(email, full_name=full_name, password=password, is_staff=True, is_admin=True)

##################################################################################################################

class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')], blank=True, null=True)
    chronic_disease = models.TextField(blank=True, null=True)
    phone_num = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\d{11}$',
                message='Phone number must be exactly 11 digits.',
                code='invalid_phone_num'
            )
        ]
    )
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

##################################################################################################################
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')], blank=True, null=True)
    chronic_disease = models.TextField(blank=True, null=True)
    phone_num = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\d{11}$',
                message='Phone number must be exactly 11 digits.',
                code='invalid_phone_num'
            )
        ]
    )

    def __str__(self):
        return str(self.user)
############################################################# [Signals] #############################################################
# Signal to sync phone_num along with other fields
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        transaction.on_commit(lambda: Profile.objects.create(
            user=instance,
            age=instance.age,
            gender=instance.gender,
            chronic_disease=instance.chronic_disease,
            phone_num=instance.phone_num
        ))
    else:
        Profile.objects.filter(user=instance).update(
            age=instance.age,
            gender=instance.gender,
            chronic_disease=instance.chronic_disease,
            phone_num=instance.phone_num
        )

# Synchronize Tokens
@receiver(post_save, sender=User)
def Token_Create_Automation(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
