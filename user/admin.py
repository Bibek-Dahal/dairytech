from django.contrib import admin

from user.models import Profile

# Register your models here.

@admin.register(Profile)
class ProfileAdminView(admin.ModelAdmin):
    list_display = ["id",'user','image','created_at','updated_at']
    # list_display_links = ("id","image")