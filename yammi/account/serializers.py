from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Profile
        fields = ('user', 'money', 'deal')


class ProfileMoneySerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Profile
        fields = ('user', 'money')


class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileMoneySerializer(many=False)

    class Meta:
        model = User
        fields = ('id', 'profile')


