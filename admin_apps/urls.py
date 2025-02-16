"""
URL configuration for admin_apps project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('the_applications.users.urls', 'login'), namespace='login')),
    path('users/', include(('the_applications.users.urls', 'users'), namespace='users')),
    path('settings/', include(('the_applications.general_settings.urls', 'general_settings'), namespace='settings')),
    path('apps/', include(('the_applications.applications.urls', 'apps'), namespace='apps')),
    path('notify/', include(('the_applications.notify.urls', 'notify'), namespace='notify')),
    path('data/', include(('the_applications.datasheet.urls', 'data'), namespace='data')),
    path('rules/', include(('the_applications.rules.urls', 'rules'), namespace='rules')),
    path('typetransport/', include(('the_applications.type_transport.urls', 'typetransport'), namespace='typetransport')),
    path('zones/', include(('the_applications.zones.urls', 'zones'), namespace='zones')),
    path('api/', include(('the_applications.api.urls', 'api'), namespace='api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
