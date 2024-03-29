from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.profile import UserProfile
from authentication.user import User
from authentication.user.serializers import UserRegistrationSerializer, UserLoginSerializer, \
    UserUpdatePasswordSerializer
from core.api_response_message import ApiResponseMessage


class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=ApiResponseMessage(_('User created succesfully')).__dict__,
                            status=status.HTTP_201_CREATED)

        return Response(data=ApiResponseMessage(_('Error while creating user')).__dict__,
                        status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(CreateAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=request.data.get('email'))
            profile = UserProfile.objects.get(user__id=user.id, is_approved=True)
            if profile is not None:
                update_last_login(None, user=user)
                refresh = RefreshToken.for_user(user)
                response = {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
                return Response(response, status=status.HTTP_200_OK)
        return Response(data=ApiResponseMessage(_('Error during login')).__dict__, status=status.HTTP_400_BAD_REQUEST)


class UserUpdatePasswordView(UpdateAPIView):
    serializer_class = UserUpdatePasswordSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            change_password_request = serializer.data
            user = User.objects.get(email=self.request.user.email)
            if user is not None and user.check_password(change_password_request['old_password']) and \
                    change_password_request['new_password'] == change_password_request['new_password_confirm']:
                user.set_password(change_password_request['new_password'])
                user.save()
                return Response(data=ApiResponseMessage(_('Password changed succesfully')).__dict__,
                                status=status.HTTP_200_OK)
        return Response(data=ApiResponseMessage(_('Error during password change')).__dict__,
                        status=status.HTTP_400_BAD_REQUEST)
