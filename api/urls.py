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


from .views import *
urlpatterns = [
    path('set-csrf-token/', set_csrf_token, name='set_csrf_token'),
    path('login/', auth_views.LoginView.as_view(template_name='api/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('users/', users_api, name='users api'),
    path('user/', user_api, name='user api'),
    path('update-profile/', update_profile_api, name='update profile api'),
    path('change-password/', change_password_api, name='change password api'),
    path('update-hobbies/', update_hobbies_api, name='update hobbies api'),
    path('fetch-hobbies/', fetch_hobbies_api, name='fetch hobbies api'),
    path('fetch-similar-users/', fetch_similar_users_api, name='fetch similar users api'),
    # The following are no longer used in the project, moved to frontend (however I haven't tested this)
    path('register/', SignUpView.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('profile/', ProfileView.as_view(), name='profile'),
    # path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('send-friend-request/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('friend-requests/', FriendRequestListView.as_view(), name='friend-requests'),
    path('friend-requests/<int:pk>/', FriendRequestActionView.as_view(), name='friend-request-action'),
]

