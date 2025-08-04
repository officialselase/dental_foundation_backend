"""
URL configuration for dental_foundation_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Import settings to access MEDIA_URL and MEDIA_ROOT 
from django.conf.urls.static import static # Import static to serve media files during development  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core_api.urls')),  # Include the core_api app's URLs
    path('ckeditor/', include('ckeditor_uploader.urls')),  # Include CKEditor URLs for file uploads
]

# Serve media files during development
# This is only for development purposes; in production, i should serve media files through a web
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
