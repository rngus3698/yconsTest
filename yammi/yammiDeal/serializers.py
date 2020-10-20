from django.contrib.auth.models import User
from rest_framework import serializers
from account.models import *
from .models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Profile
        fields = '__all__'


#profile과 join하여 불러
#유저에 대한 송금내역
class DealSerializer(serializers.ModelSerializer):
    user_give = ProfileSerializer()

    class Meta:
        model = Deal
        fields = '__all__'

#유저에 대한 송금내역
class UserDealSerializer(serializers.ModelSerializer):
    id = DealSerializer(many=True)
    # user = UserSerializer(required=True)

    class Meta:
        model = Profile
        fields = ('id', 'money', 'deal')
#유저에 대한 입금내역