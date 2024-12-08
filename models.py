from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token    # [Token Model]
from django.conf import settings
from django.utils.timezone import now

# Create your models here.
############################################################## [1] Users Profiles ##########################################################################################################################################################################################

class UserProfile(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    national_id = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, choices=[('Male','Male'),('Femal','Femal')])
    age = models.PositiveBigIntegerField(null=True, blank=True)
    choronic_disease = models.TextField(default=None, blank=True)
    
    def __str__(self):
        return str(self.patient.username)

############################################################## [2] Doctors Profile ##########################################################################################################################################################################################

class DoctorsProfileInfo(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=50)
    specialty = models.CharField(max_length=20, default=None, null=False, blank=False)
    email = models.EmailField()
    phone = models.PositiveIntegerField()
    clinic_address = models.TextField()
    bio = models.TextField(null=True, blank=True)
    img = models.ImageField(upload_to='doctors-images/', null=True, blank=True)

    def __str__(self):
        return f"{self.doctor.first_name.capitalize()} {self.doctor.last_name.capitalize()}"
    
############################################################## [3] Doctor Available Booking ##########################################################################################################################################################################################

class DoctorAvailableBooking(models.Model):
    doctor = models.ForeignKey(DoctorsProfileInfo, on_delete=models.SET_NULL, null=True)
    date_time = models.DateTimeField(default=now)
    availability = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Booking'

    def __str__(self):
        return f"{self.doctor} - {self.date_time.strftime('%Y-%m-%d %H:%M')} - {'Available' if self.availability else 'Booked'}"
    
############################################################## [4] Appointment Section ##########################################################################################################################################################################################

class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    available_booking = models.ForeignKey(DoctorAvailableBooking, on_delete=models.CASCADE, null=True, blank=True)
    date_time = models.DateTimeField(default=now)

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
        return f"Appointment booked for {self.patient.username} on {self.date_time.strftime('%Y-%m-%d %H:%M')}"

############################################################## [5] Activity Feed ##########################################################################################################################################################################################

class ActivityFeed(models.Model):
    doctor = models.ForeignKey(DoctorsProfileInfo, on_delete=models.CASCADE, null=True, blank=False)
    msg = models.TextField(blank=False, null=False, default=None)
    updated = models.DateTimeField(auto_now=True)
    complete = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.doctor)
    
################################################################################################################################################################################################################################################################################################################################
# [Signals]

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def Token_Create_Automation(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
        
################################################################################################################################################################################################################################################################################################################################

class User(models.Model):
    name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=14, unique=True)
    def __str__(self):
        return self.name
    
#######################################################################################################################################################################################################################################################################################################

class PreviousHistory(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    message = models.TextField()
    timestamp = models.DateTimeField(default=now)
    def __str__(self):
        return f"{self.sender.name if self.sender else 'Anonymous'}: {self.message[:20]}"

#######################################################################################################################################################################################################################################################################################################

class UploadedPhoto(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,)
    photo = models.ImageField(upload_to="uploaded_photos/")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo by {self.uploader.username if self.uploader else 'Anonymous'}"