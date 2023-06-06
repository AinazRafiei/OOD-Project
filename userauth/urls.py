from django.urls import path

from userauth.views import SignUpView, LoginView, LogoutView, Home

urlpatterns = [
                  path('signup/', SignUpView.as_view(), name='signup'),
                  path('login/', LoginView.as_view(), name='login'),
                  path('logout/', LogoutView.as_view(), name='logout'),
                  path('home/', Home.as_view(), name='home'),
              ]