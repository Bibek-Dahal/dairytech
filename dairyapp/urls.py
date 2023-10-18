
from django.urls import path,include
from . import views

app_name = "dairyapp"

urlpatterns = [
    path("",views.HomeView.as_view(),name="homepage"),

    #fat urls
    path("fat-rates",views.FatListView.as_view(),name="fat_list"),
    path("create-fat-rates/",views.CreateFatView.as_view(),name="create-fat"),
    path("edit-fat-rates/<uuid:id>",views.UpdateFatView.as_view(),name="edit_fat"),
    path("delete-fat-rates/<uuid:pk>",views.DeleteFatRate.as_view(),name="delete_fat"),

    #dairy urls
    path("create-dairy",views.CreateDairyView.as_view(),name="create_dairy"),
    path("list-dairy-member/<str:dairy>",views.ListDairyMembers.as_view(),name="list_dairy_members"),
    path("edit-dairy/<uuid:pk>",views.UpadteDairyView.as_view(),name="update_dairy"),
    path("list-milk-records/<str:dairy>",views.ListMilkRecords.as_view(),name="milk_record"),
    path("create-milk-records/<str:dairy>/<uuid:id>",views.CreateMilkRercord.as_view(),name="create_milk_record"),
    path("update-milk-record/<uuid:id>/<str:dairy>",views.UpdateMilkRercord.as_view(),name="update_milk_record"),
    path("list-member-milk-record/<uuid:id>/<str:dairy>",views.ListMemberMilkRecord.as_view(),name="member_milk_record"),
    path("verify-esewa",views.VerifyEsewa.as_view(),name="verify_esewa"),
    path("send-milk-report-email",views.SendMilkReportEmialView.as_view(),name="milk_report_email"),


    # khalti url
    path('initiate',views.initkhalti,name="initiate"),
    path('verify',views.verifyKhalti,name="verify")
]
