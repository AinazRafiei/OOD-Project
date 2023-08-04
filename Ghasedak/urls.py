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

from channel.views import ChannelDetailView, AllChannelsView, ChannelJoinView, \
    ChannelLeaveView, ChannelAdminsView, create_post, create_channel, show_members, ChannelTariffsView
from userauth.views import SignUpView, LoginView, LogoutView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('signup/', SignUpView.as_view(), name='signup'),
                  path('login/', LoginView.as_view(), name='login'),
                  path('logout/', LogoutView.as_view(), name='logout'),
                  path('channels/', AllChannelsView.as_view(), name='channels'),
                  path('create_channel/', create_channel, name='create_channel'),
                  path('channels/<int:channel_id>/detail', ChannelDetailView.as_view(), name='channel_details'),
                  path('channels/<int:channel_id>/admins', ChannelAdminsView.as_view(), name='channel_admins'),
                  path('channels/<int:channel_id>/tariffs', ChannelTariffsView.as_view(), name='channel_tariffs'),
                  path('channels/<int:channel_id>/members', show_members, name='show_members'),
                  path('channels/<int:channel_id>/post', create_post, name='create_post'),
                  path('channels/<int:channel_id>/join', ChannelJoinView.as_view(), name='create_post'),
                  path('channels/<int:channel_id>/leave', ChannelLeaveView.as_view(), name='create_post'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
