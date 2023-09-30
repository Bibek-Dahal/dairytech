from django.urls import path,include
from . import views
app_name = 'user'
urlpatterns = [
    path('',views.HomeView.as_view(),name='homepage'),
    path("list-member-milk-record/<str:dairy>",views.MemberMilkRecord.as_view(),name="member_milk_record"),
]