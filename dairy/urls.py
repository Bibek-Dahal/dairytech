from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('mero-dairy-admin-9846/', admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    # path('account/',include('my_account.urls',namespace='account')),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += i18n_patterns(
    path('accounts/', include('allauth.urls')),
    path('dashboard/',include("dairyapp.urls",namespace="dairyapp")),
    path('',include('user.urls',namespace='user')),
)

from django.conf.urls import handler404

handler404 = 'user.views.custom_404'

