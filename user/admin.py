from django.conf import settings
from django.contrib import admin

from user.models import Profile

# Register your models here.

@admin.register(Profile)
class ProfileAdminView(admin.ModelAdmin):
    list_display = ["id",'user','image','created_at','updated_at']
    # list_display_links = ("id","image")

from django.contrib.admin.views.decorators import staff_member_required

admin.site.login = staff_member_required(
    admin.site.login, login_url=settings.LOGIN_URL
)