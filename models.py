from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token    # [Token Model]
from django.conf import settings
from django.db import transaction
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

##################################################################################################################

class UserManager(BaseUserManager):
    def create_user(self, email, full_name=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("User must have an email address !")
        if not password:
            raise ValueError("Users must have a password !")
        # if not full_name:
        #     raise ValueError("Users must have a fullname !")
        
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
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')], blank=True, null=True)
    chronic_disease = models.TextField(blank=True, null=True)
    phone = models.CharField(
        max_length=11,
        validators=[RegexValidator(regex=r'^\d{11}$', message='Phone number must be 11 digits')],
        blank=True,
        null=True
    )  # New phone field with validation

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
    img = models.ImageField(upload_to='doctor_images/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Doctors Profile'

    def __str__(self):
        return f"{self.doc_first_name} {self.doc_last_name}"
    
##################################################################################################################
# [Signals]

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
        
@receiver(post_save, sender=User)
def Token_Create_Automation(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)



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
            
############################################################## [3] Booking ##########################################################################################################################################################################################

class Booking(models.Model):
    doctor = models.ForeignKey(DoctorsProfileInfo, on_delete=models.SET_NULL, null=True)
    date_time = models.DateTimeField(default=timezone.now)
    availability = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Booking'

    def __str__(self):
        return f"{self.doctor} - {self.date_time.strftime('%Y-%m-%d %H:%M')} - {'Available' if self.availability else 'Booked'}"
    
############################################################## [4] Appointment Section ##########################################################################################################################################################################################

class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    available_booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    date_time = models.DateTimeField(default=timezone.now)

    def clean(self):
        # Validate if the booking is already unavailable
        if self.available_booking and not self.available_booking.availability:
            raise ValidationError("This booking is unavailable.")
        
        # Validate if the same doctor and time slot are already booked
        if Appointment.objects.filter(
            available_booking__doctor=self.available_booking.doctor,
            date_time=self.date_time
        ).exclude(id=self.id).exists():
            raise ValidationError("This time slot is already booked by another patient.")

    def save(self, *args, **kwargs):
        # Call the clean method to validate before saving
        self.clean()

        # Mark the booking as unavailable
        if self.available_booking:
            self.available_booking.availability = False
            self.available_booking.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Appointment booked for {self.patient} on {self.date_time.strftime('%Y-%m-%d %H:%M')}"
    
################################################################################################################################################################################################################################################################################################################################

class DoctorAvailability(models.Model):
    pass 

############################################################## [5] Activity Feed ##########################################################################################################################################################################################

class ActivityFeed(models.Model):
    doctor = models.ForeignKey(DoctorsProfileInfo, on_delete=models.CASCADE, null=True, blank=False)
    msg = models.TextField(blank=False, null=False, default=None)
    updated = models.DateTimeField(auto_now=True)
    complete = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.doctor)
    
################################################################################################################################################################################################################################################################################################################################

class UserLogin(models.Model):
    name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=14, unique=True)
    def __str__(self):
        return self.name
    
#######################################################################################################################################################################################################################################################################################################

class PreviousHistory(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.sender.name if self.sender else 'Anonymous'}: {self.message[:20]}"

#######################################################################################################################################################################################################################################################################################################

class UploadedPhoto(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,)
    photo = models.ImageField(upload_to="uploaded_photos/")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo by {self.uploader.username if self.uploader else 'Anonymous'}"