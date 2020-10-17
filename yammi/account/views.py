from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from django.contrib.auth.models import User
from .models import models
from .serializers import *
from .models import Profile

from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
# Create your views here.


##화면전화 예시
# class signup(APIView):
#     def post(self, request):
#         userform = UserCreationForm(request.POST)
#         if userform.is_valid():
#             userform.save()
#
#             return HttpResponseRedirect(reversed("signup_ok"))
#
#     def get(self, request):
#         userform = UserCreationForm()
#         return render(request, "registration/signup.html", {"userform": userform})

class SignupView(APIView):
    #회원전체 조회
    def get(self, format=None):
        profile = Profile.objects.all() #Profile객체의 전체를 뽑아온다
        serializer = ProfileSerializer(profile, many=True)  #뽑아온 Profile 객체를 Json 타입으로 변환
        return Response(serializer.data)

    #회원가입
    def post(self, request):
        # profile = Profile.objects.get(userame=request.data['username'])  #username 중복체크

        user = User.objects.create_user(username=request.data['username'], password=request.data["password"])
        profile = models.Profile(user=user, money=500)

        user.save()
        profile.save()

        token = Token.objects.create(user=user)
        print(token.key)
        return Response({"Token": token.key})


class LoginView(APIView):
    def post(self, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user is not None:
            token = Token.objects.get(user=user)
            return Response({"Token": token.key})   #로그인 성공후 토큰을 가져온다.
        else:
            return Response(status=401) #로그인 실패