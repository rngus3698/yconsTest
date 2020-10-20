from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Deal


# Create your views here.


class DealView(APIView):
    permission_classes = [IsAuthenticated]
    # JWT 인증을 확인하기 위해 사용한다
    authentication_classes = [JSONWebTokenAuthentication]

    def get(self, request):
        my_deal = Deal.objects.all() #Profile객체의 전체를 뽑아온다
        serializer = DealSerializer(my_deal, many=True)  #뽑아온 Profile 객체를 Json 타입으로 변환
        return Response(serializer.data)

    def post(self, request):

        my_profile = Profile.objects.get(user_id=request.data["user_id"])

        deal_obj = Deal.objects.create(user_take=request.data["user_profile_take"],
                                       deal_money=request.data["deal_money"], user_give=my_profile)

        deal_obj.save()

        print(request.POST)

        # give_serializer = ProfileSerializer(my_profile)
        # # money = give_serializer.data["money"]-request.data["deal_money"]
        # give_user = Profile.objects.update(#id=give_serializer.data["id"],
        #                                    money=1500,
        #                                    user_id=request.data["user_id"])
        #
        # take_profile = Profile.objects.get(user_id=request.dta["user_profile_take"])
        # take_serializer = ProfileSerializer(take_profile)
        # # money = take_serializer.data["money"]+request.data["deal_money"]
        # take_user = Profile.objects.update(#id=request.data["user_profile_take"],
        #                                    money=200,
        #                                    user_id=take_serializer.data["user_id"])
        # give_user.save()
        # take_user.save()
        return Response({"거래": "성공"})

    # def put(self, request):
    #     my_profile = Profile.objects.get(user_id=request.data["user_id"])
    #     serializer = ProfileSerializer(my_profile)
    #     my_profile_ch = Profile.objects.update(user_id=serializer.data["user_id"], money=serializer.data["money"]+request.data["money"])
    #     my_profile_ch.save()
    #
    #     return Response()


class DetailDeal(APIView):
    permission_classes = [IsAuthenticated]
    # JWT 인증을 확인하기 위해 사용한다
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request):    #해당 유저의 송금, 입금 리스트 뽑
        user_id = request.data["user_id"]
        my_give_deal = Deal.objects.filter(user_give_id=user_id) | Deal.objects.filter(user_take=user_id)
        serializer = DealSerializer(my_give_deal, many=True)

        return Response(serializer.data)

