from django.urls import path

from channel.views import create_channel, create_post

urlpatterns = [
                  path('create_channel/', create_channel, name='create_channel'),
                  path('create_post/', create_post, name='create_post'),
              ]