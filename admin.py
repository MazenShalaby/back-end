from django.contrib import admin
from .models import Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
##################################################################################################################

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ['email', 'created_at', 'last_login', 'admin', 'active']
    list_filter = ['active', 'staff', 'admin']

    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Personal info', {'fields': ('full_name', 'age', 'gender', 'chronic_disease', 'phone_num')}),  # Include phone number
        ('Permissions', {'fields': ('active', 'staff', 'admin')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'phone_num')
        }),
    )

    search_fields = ['email', 'full_name']
    ordering = ['email']
    filter_horizontal = ()

    def get_fieldsets(self, request, obj=None):
        # If permissions are all True, remove the 'Personal info' fields
        if obj and obj.admin and obj.staff and obj.active:
            return (
                (None, {'fields': ('email', 'password',)}),
                ('Permissions', {'fields': ('active', 'staff', 'admin')}),
            )
        return super().get_fieldsets(request, obj)

##########################################################[Register]########################################################

# Register the custom user model with the admin site
admin.site.register(User, UserAdmin)
# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)

class UserProfileSearch(admin.ModelAdmin):
    search_fields = ['user__email']
    class Meta:
        model = Profile
admin.site.register(Profile, UserProfileSearch)