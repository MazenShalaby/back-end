from django.contrib import admin
from .models import (
    Profile, DoctorsProfileInfo, Appointment, ActivityFeed, 
    UserLogin, PreviousHistory, UploadedPhoto, DoctorAvailability
)
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm

# Get the custom User model
User = get_user_model()

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ['email', 'created_at', 'last_login', 'admin', 'active', 'staff', 'phone']
    list_filter = ['active', 'staff', 'admin']
    search_fields = ['email', 'full_name', 'phone']
    ordering = ['email']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'age', 'gender', 'chronic_disease', 'phone')
        }),
        ('Permissions', {'fields': ('active', 'staff', 'admin')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2',
                'first_name', 'last_name', 'age', 'gender', 'chronic_disease', 'phone'
            ),
        }),
    )

    filter_horizontal = ()

    def save_model(self, request, obj, form, change):
        """
        Custom save logic for UserAdmin.
        """
        super().save_model(request, obj, form, change)

        # Create or update Profile
        if obj.active and not obj.admin and not obj.staff:
            profile, created = Profile.objects.get_or_create(user=obj)
            profile.first_name = obj.first_name
            profile.last_name = obj.last_name
            profile.phone = obj.phone
            profile.age = obj.age
            profile.gender = obj.gender
            profile.chronic_disease = obj.chronic_disease
            profile.save()

        # Delete Profile if user is promoted
        elif obj.admin or obj.staff:
            if hasattr(obj, 'profile'):
                obj.profile.delete()

# Register the custom UserAdmin
admin.site.register(User, UserAdmin)
# Unregister the Group model
admin.site.unregister(Group)

#############################################################################################################

# DoctorsProfileInfo Admin
class DoctorsProfileInfoAdmin(admin.ModelAdmin):
    search_fields = ['doc_first_name', 'doc_last_name', 'phone', 'specialty']
    list_display = ['doc_first_name', 'doc_last_name', 'specialty', 'phone']
    ordering = ['doc_last_name']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Filter the 'user' field to show only available users with the correct permissions.
        """
        if db_field.name == "user":
            used_users = DoctorsProfileInfo.objects.values_list('user', flat=True)
            kwargs["queryset"] = User.objects.filter(admin=False, staff=True, active=True)#.exclude(id__in=used_users)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(DoctorsProfileInfo, DoctorsProfileInfoAdmin)

#############################################################################################################

# PreviousHistory Admin
class PreviousHistoryAdmin(admin.ModelAdmin):
    list_display = ['sender', 'message_preview', 'timestamp']
    search_fields = ['sender__email', 'message']
    ordering = ['-timestamp']

    def get_form(self, request, obj=None, **kwargs):
        """
        Customizes the form for the PreviousHistory model to filter the sender field.
        """
        form = super().get_form(request, obj, **kwargs)
        sender_field = form.base_fields.get('sender')
        if sender_field:
            # Filtering only users with doctor permissions => [admin=False, staff=True, active=True]
            sender_field.queryset = User.objects.filter(admin=False, staff=True, active=True)
        return form

    def message_preview(self, obj):
        """
        Displays a preview of the message content in the admin list view.
        """
        return obj.message[:50] if obj.message else ""

    message_preview.short_description = "Message Preview"

admin.site.register(PreviousHistory, PreviousHistoryAdmin)

#############################################################################################################

# Appointment Admin
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'available_booking', 'date_time', 'doctor']
    search_fields = ['patient__email', 'date_time']
    ordering = ['date_time']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Filter the 'patient' field to show only users with the correct permissions.
        """
        if db_field.name == "patient":
            kwargs["queryset"] = User.objects.filter(admin=False, staff=False, active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Appointment, AppointmentAdmin)

#############################################################################################################

# DoctorAvailability Admin
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'day', 'start_time', 'end_time', 'availability']
    list_filter = ['doctor', 'day', 'availability']
    search_fields = ['doctor__doc_first_name', 'doctor__doc_last_name', 'day']
    ordering = ['doctor', 'day', 'start_time']
    list_per_page = 10  # Optional: Controls how many items to display per page
    
    # Customizing the form to filter doctors based on specific permissions
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "doctor":
            # Only allow doctors that have the correct permissions
            kwargs["queryset"] = DoctorsProfileInfo.objects.filter(user__admin=False, user__staff=True, user__active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        """
        Custom save logic for DoctorAvailability.
        - Ensure the validation for start and end time is applied.
        - You can add more custom logic here if needed.
        """
        obj.clean()  # Make sure custom validation is triggered
        super().save_model(request, obj, form, change)

# Register the DoctorAvailability model with the custom admin
admin.site.register(DoctorAvailability, DoctorAvailabilityAdmin)

#############################################################################################################

# Profile Admin
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'phone', 'age', 'gender', 'chronic_disease']
    list_filter = ['gender', 'age']
    search_fields = ['user__email', 'first_name', 'last_name', 'phone']
    ordering = ['user']
    list_per_page = 10  # Optional: Controls how many items to display per page

    def save_model(self, request, obj, form, change):
        """
        Custom save logic for Profile.
        - Ensure that any necessary validation or additional logic is triggered.
        """
        # Custom logic can be added here if needed
        super().save_model(request, obj, form, change)

# Register the Profile model with the custom admin
admin.site.register(Profile, ProfileAdmin)

#############################################################################################################

# Register other models
admin.site.register(UserLogin)
admin.site.register(ActivityFeed)
admin.site.register(UploadedPhoto)