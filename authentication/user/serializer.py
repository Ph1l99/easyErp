from django.contrib.auth import authenticate
from rest_framework import serializers

from authentication.profile import UserProfile
from authentication.user import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'username']


class UserRegistrationSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile = validated_data.pop('profile')

        user = User.object.create_user(**validated_data)
        UserProfile.objects.create(
            user=user,
            first_name=profile['first_name'],
            last_name=profile['last_name'],
            username=profile['username']
        )
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError('User Not Found')
        return user
