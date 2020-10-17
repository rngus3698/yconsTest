from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from django.contrib.auth.models import User
from .models import models
from .serializers import *
from .models import Profile
from rest_framework.permissions import IsAuthenticated

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
        return Response({"Token": token})


class LoginView(APIView):
    def post(self, request):
        #Authentication은 수신 요청을 요청한 사용자 또는 서명 된 토큰과 같은 식별 자격 증명 세트를 연결하는 메커니즘입니다.
        #그런 다음 권한과 정책은 이러한 자격 증명을 사용하여 요청을 허용해야 하는지 결정할 수 있습니다.
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user is not None:
            token = Token.objects.get(user=user)
            return Response({"Token": token.key})   #로그인 성공후 토큰을 가져온다.
        else:
            return Response(status=401) #로그인 실패


##토큰을 통해 정상적으로 데이터를 가져올 수 있는지 확인
class UserInfo(APIView):

    ###UserInfo API는 로그인한 사용자에게만 접근이 허용된다.
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        username = request.query_params.get("username")
        query = User.objects.get(username=username)

        serializer = UserSerializer(query, many=False)

        return Response(serializer.data)
