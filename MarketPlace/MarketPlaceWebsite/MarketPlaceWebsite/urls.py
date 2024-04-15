from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from Website.views import (
    register_view,
    profile_view,
    update_username_view,
    update_password_view
)

urlpatterns = [
    path('', include('Website.urls')),
    path('admin/', admin.site.urls),
    path('Website/', include('Website.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('user/profile/', profile_view, name='profile'),
    path('user/update-username/', update_username_view, name='update_username'),
    path('user/update-password/', update_password_view, name='update_password'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
