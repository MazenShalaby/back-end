from django.contrib import admin
from .models import UserProfile ,DoctorsProfileInfo , Appointment, DoctorAvailableBooking, ActivityFeed, User, PreviousHistory, UploadedPhoto

admin.site.register(UserProfile)
admin.site.register(DoctorsProfileInfo)
admin.site.register(DoctorAvailableBooking)
admin.site.register(Appointment)
admin.site.register(ActivityFeed)

admin.site.register(User)
admin.site.register(PreviousHistory)
admin.site.register(UploadedPhoto)


