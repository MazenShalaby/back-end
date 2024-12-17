from django.contrib import admin
from .models import Profile, DoctorsProfileInfo, Appointment, DoctorAvailableBooking, ActivityFeed, UserLogin, PreviousHistory, UploadedPhoto
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

    def get_fieldsets(self, request, obj=None):
        if obj and obj.admin and obj.staff and obj.active:
            return (
                (None, {'fields': ('email', 'password',)}),
                ('Permissions', {'fields': ('active', 'staff', 'admin')}),
            )
        return super().get_fieldsets(request, obj)

    def save_model(self, request, obj, form, change):
        """
        Custom save logic for UserAdmin.
        If the user is active and not an admin, create or update their Profile.
        If promoted to admin, remove their Profile.
        """
        super().save_model(request, obj, form, change)

        if (obj.admin and obj.staff and obj.active) or (obj.staff and obj.active):
            # Remove the Profile if the user becomes an admin or staff
            if hasattr(obj, 'profile'):
                obj.profile.delete()
        elif obj.active:  
            # Create or update Profile if user is active but not an admin
            profile, created = Profile.objects.get_or_create(user=obj)
            profile.first_name = obj.first_name
            profile.last_name = obj.last_name
            profile.phone = obj.phone
            profile.age = obj.age
            profile.gender = obj.gender
            profile.chronic_disease = obj.chronic_disease
            profile.save()


# Register the custom UserAdmin with the admin site
admin.site.register(User, UserAdmin)
# Unregister the Group model as it's not used
admin.site.unregister(Group)

# Admin customization for the Profile model
class UserProfileSearch(admin.ModelAdmin):
    search_fields = ['user__email']  # Allow searching by user email

admin.site.register(Profile, UserProfileSearch)

########################################################################################################

class DoctorsProfileInfoAdmin(admin.ModelAdmin):
    search_fields = ['doc_first_name', 'doc_last_name', 'phone', 'specialty']
    list_display = ['doc_first_name', 'doc_last_name', 'specialty', 'phone']
    ordering = ['doc_last_name']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Filter the 'user' field to show only users with [admin=False, staff=True, active=True],
        and exclude users who already have a doctor profile.
        """
        if db_field.name == "user":
            # Exclude users who already have a DoctorProfileInfo instance
            existing_doctors = DoctorsProfileInfo.objects.values_list('user', flat=True)
            kwargs["queryset"] = User.objects.filter(admin=False, staff=True, active=True).exclude(id__in=existing_doctors)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(DoctorsProfileInfo, DoctorsProfileInfoAdmin)

########################################################################################################

admin.site.register(UserLogin)

admin.site.register(DoctorAvailableBooking)
admin.site.register(Appointment)

admin.site.register(ActivityFeed)
admin.site.register(PreviousHistory)
admin.site.register(UploadedPhoto)


