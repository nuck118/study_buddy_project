from django.contrib import admin
from django.urls import path, include
from django.conf import settings # <--- New
from django.conf.urls.static import static # <--- New

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
]

# This allows images to show up while you are coding (Debug mode)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)