from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.exceptions import NotFound as NotFoundError
from rest_framework import status

from .models import Deal
from rest_framework.pagination import PageNumberPagination


# Create your views here.


class MyPageNumberPagination(PageNumberPagination):
   page_size = 10

   def generate_response(self, query_set, serializer_obj, request):
       try:
           page_data = self.paginate_queryset(query_set, request)
       except NotFoundError:
           return Response({"error": "No results found for the requested page"}, status=status.HTTP_400_BAD_REQUEST)

       serialized_page = serializer_obj(page_data, many=True)
       return self.get_paginated_response(serialized_page.data)


class DealView(APIView):
    permission_classes = [IsAuthenticated]
    # JWT 인증을 확인하기 위해 사용한다
    authentication_classes = [JSONWebTokenAuthentication]

    def get(self, request):
        queryset = Deal.objects.all() #Profile객체의 전체를 뽑아온다
        serializer = DealSerializer(queryset, many=True)  #뽑아온 Profile 객체를 Json 타입으로 변환
        return Response(serializer.data)

    def post(self, request):

        my_profile = Profile.objects.get(user_id=request.data["user_id"])

        print(int(request.data["deal_money"]))
        #주는사람 profile update
        my_profile.money = my_profile.money - int(request.data["deal_money"])
        if(my_profile.money < 0):   #주는 금액이 가지고있는 금액을 초과하면 return
            return Response({"거래": "실패"})
        else:
            my_profile.save()
        #받는사람
        take_profile = Profile.objects.get(user_id=request.data["user_profile_take"])
        take_profile.money = take_profile.money + int(request.data["deal_money"])
        take_profile.save()

        #Deal 테이블 insert
        deal_obj = Deal.objects.create(user_take=request.data["user_profile_take"],
                                       deal_money=request.data["deal_money"], user_give=my_profile)

        deal_obj.save()

        return Response({"거래": "성공"})


class DetailDeal(APIView):
    permission_classes = [IsAuthenticated]
    # JWT 인증을 확인하기 위해 사용한다
    authentication_classes = [JSONWebTokenAuthentication]
    pagination_class = PageNumberPagination

    def post(self, request):    #해당 유저의 송금, 입금 리스트 뽑
        user_id = request.data["user_id"]
        queryset = Deal.objects.filter(user_give_id=user_id) | Deal.objects.filter(user_take=user_id)
        paginator = MyPageNumberPagination()
        response = paginator.generate_response(queryset, DealSerializer, request)

        return response

