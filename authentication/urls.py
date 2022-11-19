from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from authentication.profile.views import UserProfileView
from authentication.user.views import UserRegistrationView

urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_obtain_refresh'),
    path('signup', UserRegistrationView.as_view(), name='signup'),
    path('profile', UserProfileView.as_view(), name='profile')
]
