"""
URL configuration for Ghasedak project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from userauth.views import SignUpView, LoginView, LogoutView, Home

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('signup/', SignUpView.as_view(), name='signup'),
                  path('login/', LoginView.as_view(), name='login'),
                  path('logout/', LogoutView.as_view(), name='logout'),
                  path('home/', Home.as_view(), name='home'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
