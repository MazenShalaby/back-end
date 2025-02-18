from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
##################################################################################################################

class UserManager(BaseUserManager):
    def create_user(self, email, full_name=None, password=None, is_active=True, is_staff=False, is_admin=False, is_superuser=False):
        if not email:
            raise ValueError("User must have an email address!")
        if not password:
            raise ValueError("Users must have a password!")
        
        user_obj = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
        )
        user_obj.active = is_active
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.is_superuser = is_superuser
        user_obj.set_password(password)
        user_obj.full_clean()  # Validate fields before saving
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, full_name=None, password=None):
        return self.create_user(email, full_name=full_name, password=password, is_staff=True)

    def create_superuser(self, email, full_name=None, password=None):
        return self.create_user(email, full_name=full_name, password=password, is_staff=True, is_admin=True, is_superuser=True)

class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')], blank=True, null=True)
    chronic_disease = models.TextField(blank=True, null=True)
    phone = models.CharField(
        max_length=11,
        unique=True,
        validators=[RegexValidator(regex=r'^\d{11}$', message='Phone number must be 11 digits')],
        blank=True,
        null=True,
    )
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    # Custom fields
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
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

    def clean(self):
        """
        Custom validation to ensure the phone number is unique.
        """
        if self.phone and User.objects.exclude(pk=self.pk).filter(phone=self.phone).exists():
            raise ValidationError({"phone": "This phone number is already in use."})

##################################################################################################################

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(
        max_length=11,
        validators=[RegexValidator(regex=r'^\d{11}$', message='Phone number must be 11 digits')],
        blank=True,
        null=True
    )
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')], blank=True, null=True)
    chronic_disease = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(blank=True, null=True)

    class Meta:
        verbose_name = 'Patients Profile'

    def __str__(self):
        return str(self.user)
    
##################################################################################################################

class DoctorsProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    doc_first_name = models.CharField(max_length=100)
    doc_last_name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=11,
        unique=True,  # Enforces uniqueness at the database level
        validators=[
            RegexValidator(
                regex=r'^\d{11}$',
                message="Phone number must consist of exactly 11 digits and be numeric."
            )
        ],
        help_text="Enter a valid 11-digit phone number (numeric only)."
    )
    clinic_address = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    img = models.ImageField(upload_to='doc-imgs/', blank=True, null=True)

    class Meta:
        verbose_name = 'Doctors Profile'

    def clean(self):
        """
        Custom validation to ensure the phone number is unique.
        """
        if DoctorsProfileInfo.objects.exclude(pk=self.pk).filter(phone=self.phone).exists():
            raise ValidationError({"phone": "This phone number is already in use by another doctor."})

    def save(self, *args, **kwargs):
        """
        Overrides save to ensure `clean` is called before saving.
        """
        self.full_clean()  # Runs validations including `clean`
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.doc_first_name} {self.doc_last_name}"
    
############################################################## [3] Doctor Availability ##########################################################################################################################################################################################

class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(DoctorsProfileInfo, on_delete=models.CASCADE)
    department = models.CharField(
        max_length=100,
        choices = [
            ('اخصائي سكر الاطفال','اخصائي سكر الاطفال'),
            ('اخصائي علاج طبيعي','اخصائي علاج طبيعي'),
            ('اخصائي امراض القلب','اخصائي امراض القلب'),
            ]
        )
    date = models.DateField(default=None, blank=True, null=True)
    start_time = models.TimeField(default=None, blank=True, null=True)
    end_time = models.TimeField(default=None, blank=True, null=True)

    class Meta:
        verbose_name = 'Doctors Availabilitie'

    def __str__(self):
        return f"{self.doctor} ==> {self.date}"

############################################################## [4] Book an Appointment ##########################################################################################################################################################################################

class Booking_Appointments(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorsProfileInfo, on_delete=models.CASCADE)
    date = models.DateField(default=None, blank=False, null=False)
    time = models.TimeField()
    available = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Book an appointment'

    def __str__(self):
        return f"Appointment for {self.patient} with Dr. {self.doctor} on {self.date} at {self.time}"

    def save(self, *args, **kwargs):
        # When saving the appointment, set the available field to False
        if self.available:  # If appointment is available, mark it as unavailable after saving
            self.available = False
        super().save(*args, **kwargs)


############################################################################# [Badr's Model] ###################################################################################################################################################################################################################################################

class PreviousHistory(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="messages"
    )
    reciever = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="received_messages"
    )
    message = models.TextField(max_length=100, blank=False, null=False)
    timestamp = models.TimeField(blank=True, null=True, auto_now_add=True)

    def __str__(self):
        return f"{self.sender.email if self.sender else 'Anonymous'}: {self.message[:20]}"

    def clean(self):
        """
        Custom validation to ensure that the sender is an active staff member (doctor).
        """
        if self.sender:  # Check if the sender is not null
            if not (self.sender.staff and self.sender.active):
                raise ValidationError("The sender must be an active staff member (doctor).")

    class Meta:
        verbose_name_plural = "Previous Histories"

#######################################################################################################################################################################################################################################################################################################

class UploadedPhoto(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,)
    photo = models.ImageField(upload_to="uploaded_photos/", default=None)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Uploaded Photo'

    def __str__(self):
        return f"Photo by {self.uploader if self.uploader else 'Anonymous'}"
        
#######################################################################################################################################################################################################################################################################################################
    
class Alarm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pill_name = models.CharField(max_length=100)
    alarm_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pill_name} - {self.alarm_time}"
    
######################################################################  [signals]  #################################################################################################################################################################################################################################
    
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token    # [Token Model]
from django.conf import settings 

########################################################### [1] User Model Signal ###################################################

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Creates or updates the PatientsProfile instance linked to the User, excluding superusers.
    """
    if instance.is_superuser:  # Skip superusers
        return

    if created:
        Profile.objects.create(
            user=instance,
            age=instance.age,
            gender=instance.gender,
            chronic_disease=instance.chronic_disease,
            phone=instance.phone,
        )
    else:
        # Update profile if it exists
        Profile.objects.update_or_create(
            user=instance,
            defaults={
                'age': instance.age,
                'gender': instance.gender,
                'chronic_disease': instance.chronic_disease,
                'phone': instance.phone,
            }
        )

########################################################### [2] Token Signal ########################################################

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def Token_Create_Automation(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)

########################################################### [3] Patient Profile Signal ##############################################

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # Exclude superusers, admins, and doctors (staff members)
    if not instance.is_superuser and not instance.is_admin and not instance.is_staff:
        if created:
            # Create a profile only if it doesn't already exist
            Profile.objects.get_or_create(
                user=instance,
                defaults={
                    'first_name': instance.first_name,
                    'last_name': instance.last_name,
                    'phone': instance.phone,
                    'age': instance.age,
                    'gender': instance.gender,
                    'chronic_disease': instance.chronic_disease,
                    'profile_picture': instance.profile_picture  # Copy profile picture from User to Profile
                }
            )
        else:
            # Update profile if it exists
            if hasattr(instance, 'profile'):
                instance.profile.first_name = instance.first_name
                instance.profile.last_name = instance.last_name
                instance.profile.phone = instance.phone  
                instance.profile.age = instance.age
                instance.profile.gender = instance.gender
                instance.profile.chronic_disease = instance.chronic_disease
                instance.profile.profile_picture = instance.profile_picture  # Update profile picture
                instance.profile.save()
    else:
        # If the user is a superuser, admin, or doctor, delete their profile if it exists
        if hasattr(instance, 'profile'):
            instance.profile.delete()
#######################################################################################################################################################################################################################################################################################################