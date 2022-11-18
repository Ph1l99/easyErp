from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.user.views import UserRegistrationView

urlpatterns = [
    path('token/refresh', TokenRefreshView.as_view()),
    path('signup', UserRegistrationView.as_view())
]
