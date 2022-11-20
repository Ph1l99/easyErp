from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.profile.views import UserProfileView
from authentication.user.views import UserRegistrationView, UserLoginView, UserUpdatePasswordView

urlpatterns = [
    path('token/refresh', TokenRefreshView.as_view(), name='token_obtain_refresh'),

    path('login', UserLoginView.as_view(), name='login'),
    path('signup', UserRegistrationView.as_view(), name='signup'),

    path('profile', UserProfileView.as_view(), name='profile'),
    path('profile/password', UserUpdatePasswordView.as_view(), name='profile_password')
]
