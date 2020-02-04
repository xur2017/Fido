"""fido_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views #1


urlpatterns = [
    path('admin/', admin.site.urls),
    #path(r'^api-auth/', include('rest_framework.urls')),
    path('', include('pet.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('oauth/', include('social_django.urls', namespace='social')), #1
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#1. https://simpleisbetterthancomplex.com/tutorial/2016/10/24/how-to-add-social-login-to-django.html
