from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include("account.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("service/", include("service.urls")),
    path("shop/", include("accessories.urls")),
    path("", include("base.urls")),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="base/main.html"),
        name="logout",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
