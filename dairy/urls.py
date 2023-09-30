from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    # path('account/',include('my_account.urls',namespace='account')),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += i18n_patterns(
    path('accounts/', include('allauth.urls')),
    path('dashboard/',include("dairyapp.urls",namespace="dairyapp")),
    path('',include('user.urls',namespace='user')),
)