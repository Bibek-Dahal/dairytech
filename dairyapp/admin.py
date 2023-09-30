from django.contrib import admin


from .models import *
# Register your models here.

@admin.register(Dairy)
class DairyAdmin(admin.ModelAdmin):
    list_display = ["name","user","location","is_verified"]
    search_fields = ["name"]

@admin.register(FatRate)
class FatRateAdmin(admin.ModelAdmin):
    list_display = ["id","fat_rate","dairy","created_at","updated_at"]

@admin.register(MilkRecord)
class MilkRecord(admin.ModelAdmin):
    list_display = ["id","dairy","user","shift","date","created_at","updated_at"]

@admin.register(MilkReportEmailHistory)
class MilkReportEmailHistoryAdmin(admin.ModelAdmin):
    list_display = ['user','dairy','shift','fat_rate','bonous_amount','milk_weight','avg_fat','total_amount','start_date','end_date']
