from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import MyUserCreationForm,MyUserChangeForm
from my_account.models import User
from django.utils.translation import gettext_lazy as _

class UserAdmin(BaseUserAdmin): 
    # The forms to add and change user instances
    form = MyUserChangeForm
    add_form = MyUserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["id","first_name","middle_name","last_name","email","phone_number","address","has_verified_dairy","is_superuser","is_staff"]
    list_filter = ["is_superuser","is_active"]
    fieldsets = [
        (None, {"fields": ["first_name","last_name","password","middle_name","email","has_verified_dairy","phone_number","is_email_verified"]}),
        ("Personal info", {"fields": ["address"]}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["phone_number","email","first_name","middle_name","last_name","password1", "password2","address"],
            },
        ),
    ]
    search_fields = [_("email"),_("phone_number")]
    ordering = ["first_name"]
    filter_horizontal = []


admin.site.register(User, UserAdmin)