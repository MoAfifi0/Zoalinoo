from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]


urlpatterns += i18n_patterns(
    path("", include("pages.urls")),
    path("accounts/", include("accounts.urls")),
    path("products/", include("products.urls")),
    path("orders/", include("orders.urls")),
    path("admin/", admin.site.urls),
 ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
