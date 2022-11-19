from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.profile import UserProfile
from authentication.profile.serializers import UserProfileSerializer


class UserProfileView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response(UserProfileSerializer(UserProfile.objects.get(user__id=self.request.user.id)).data,
                        status=status.HTTP_200_OK)
