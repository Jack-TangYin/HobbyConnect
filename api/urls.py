"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
from django.contrib.auth import views as auth_views
from .views import SimilarUsersView, SendFriendRequestView


from .views import SignUpView, ProfileView, EditProfileView, users_api, user_api, logout_view, set_csrf_token
urlpatterns = [
    path('set-csrf-token/', set_csrf_token, name='set_csrf_token'),
    path('login/', auth_views.LoginView.as_view(template_name='api/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('users/', users_api, name='users api'),
    path('user/', user_api, name='user api'),
    # The following are no longer used in the project, moved to frontend (however I haven't tested this)
    path('register/', SignUpView.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('api/send-friend-request/', SendFriendRequestView.as_view(), name='send-friend-request'),
]
