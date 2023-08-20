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
from django.urls import path

from channel.views import ChannelDetailView, AllChannelsView, ChannelJoinView, \
    ChannelLeaveView, ChannelAdminsView, ChannelTariffsView, SubscribeView, create_post, create_channel, show_members, \
    PurchasePostView, SearchChannelView

urlpatterns = [
    path('', AllChannelsView.as_view(), name='channels'),
    path('create', create_channel, name='create_channel'),
    path('<int:channel_id>/detail', ChannelDetailView.as_view(), name='channel_details'),
    path('<int:channel_id>/admins', ChannelAdminsView.as_view(), name='channel_admins'),
    path('<int:channel_id>/tariffs', ChannelTariffsView.as_view(), name='channel_tariffs'),
    path('<int:channel_id>/members', show_members, name='show_members'),
    path('<int:channel_id>/post', create_post, name='create_post'),
    path('<int:channel_id>/posts/<int:post_id>/purchase', PurchasePostView.as_view(), name='purchase_post'),
    path('<int:channel_id>/join', ChannelJoinView.as_view(), name='create_post'),
    path('<int:channel_id>/leave', ChannelLeaveView.as_view(), name='create_post'),
    path('<int:channel_id>/subscribe', SubscribeView.as_view(), name='subscribe'),
    path('search/<str:channel_name>', SearchChannelView.as_view(), name='search_channel'),
]
