from django.urls import path,include
from . import views
# app_name = 'account'

urlpatterns = [
    path('register/',views.RegView.as_view(),name="register"),
    path('login/',views.RegisterView.as_view(),name="login"),
]