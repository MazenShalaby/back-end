from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
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

    # Custom fields
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    # Add `is_superuser` field for Django's permission system
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
    day = models.CharField(
        max_length=10,
        choices=[
            ('Sun', 'Sunday'),
            ('Mon', 'Monday'),
            ('Tue', 'Tuesday'),
            ('Wed', 'Wednesday'),
            ('Thu', 'Thursday'),
            ('Fri', 'Friday'),
            ('Sat', 'Saturday'),
        ]
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        verbose_name = 'Doctors Appointment'

    def __str__(self):
        return f"{self.doctor} - {self.day} ({self.start_time.strftime('%H:%M')} to {self.end_time.strftime('%H:%M')})"

    def clean(self):
        """
        Custom validation to ensure the start time is before the end time and no overlap exists.
        """
        if self.start_time >= self.end_time:
            raise ValidationError("The start time must be before the end time.")
        
        # Validate overlapping slots for the same doctor and day
        overlapping_slots = DoctorAvailability.objects.filter(
            doctor=self.doctor,
            day=self.day,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(id=self.id)
        if overlapping_slots.exists():
            raise ValidationError("This time slot overlaps with another availability for this doctor.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
############################################################## [4] Booking Appointment Section ##########################################################################################################################################################################################

class Booking_Appointments(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    available_booking = models.ForeignKey(DoctorAvailability, on_delete=models.CASCADE, null=True, blank=True)
    date_time = models.DateTimeField()
    doctor = models.ForeignKey(DoctorsProfileInfo, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Book An Appointment'

    def clean(self):
        """
        Ensure the appointment time falls within available hours and isn't double-booked.
        """
        if not self.available_booking:
            raise ValidationError("You must select an available booking.")

        availability = self.available_booking

        # Validate time within available hours
        if not (availability.start_time <= self.date_time.time() < availability.end_time):
            raise ValidationError(
                f"Appointment time must be between {availability.start_time.strftime('%H:%M')} "
                f"and {availability.end_time.strftime('%H:%M')} on {availability.day}."
            )

        # Check for double booking
        if Booking_Appointments.objects.filter(
            available_booking=availability,
            date_time=self.date_time
        ).exclude(id=self.id).exists():
            raise ValidationError("This time slot is already booked.")

    def save(self, *args, **kwargs):
        self.clean()

        # Update availability if the slot is booked
        if self.available_booking.availability:
            self.available_booking.availability = False
            self.available_booking.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Override delete to restore availability when an appointment is canceled.
        """
        if self.available_booking:
            self.available_booking.availability = True
            self.available_booking.save()
        
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Appointment for {self.patient} with Dr. {self.doctor} on {self.date_time.strftime('%Y-%m-%d %H:%M')}"

################################################################################################################################################################################################################################################################################################################################
# class Appoinmnets(models.Model):
    
#     patient = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     doctor = models.ForeignKey(DoctorsProfileInfo, on_delete=models.CASCADE)
#     appoinmnet_date = models.DateTimeField()
#     appoinmnet_time = models.TimeField()
    
    
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
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

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
    photo = models.ImageField(upload_to="uploaded_photos/")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Uploaded Photo'

    def __str__(self):
        return f"Photo by {self.uploader.username if self.uploader else 'Anonymous'}"
        
#######################################################################################################################################################################################################################################################################################################
    
class Alarm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pill_name = models.CharField(max_length=100)
    alarm_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pill_name} - {self.alarm_time}"
    
######################################################################  [signals]  #################################################################################################################################################################################################################################
    
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
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

def create_or_update_user_profile(sender, instance, created, **kwargs):
    # Create profile if it doesn't exist
    if created:
        Profile.objects.create(user=instance)
    else:
        # Update profile if it exists
        if hasattr(instance, 'profile'):
            instance.profile.first_name = instance.first_name
            instance.profile.last_name = instance.last_name
            instance.profile.phone = instance.phone  
            instance.profile.age = instance.age
            instance.profile.gender = instance.gender
            instance.profile.chronic_disease = instance.chronic_disease
            instance.profile.save()
            