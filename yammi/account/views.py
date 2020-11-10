from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib.auth import authenticate

from .serializers import *
from .models import Profile
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


from django.http import HttpResponseRedirect
# Create your views here.


class SignupView(APIView):
    permission_classes = [AllowAny]
    #회원전체 조회
    def get(self, format=None):
        profile = Profile.objects.all() #Profile객체의 전체를 뽑아온다
        serializer = ProfileSerializer(profile, many=True)  #뽑아온 Profile 객체를 Json 타입으로 변환
        return Response(serializer.data)

    #회원가입
    def post(self, request):

        if User.objects.filter(username=request.data['id']).exists():
            return Response({"회원가입": "아이디가 중복됩니다."})

        else:
            user = User.objects.create_user(username=request.data['id'],
                                            password=request.data["password"],
                                            first_name=request.data["username"])

            user.save()

            return Response({"회원가입": "성공"})


class LoginView(APIView):
    permission_classes = [AllowAny]
    # renderer_classes = [TemplateHTMLRenderer]
    def post(self, request):
        #Authentication은 수신 요청을 요청한 사용자 또는 서명 된 토큰과 같은 식별 자격 증명 세트를 연결하는 메커니즘입니다.
        #그런 다음 권한과 정책은 이러한 자격 증명을 사용하여 요청을 허용해야 하는지 결정할 수 있습니다.
        user = authenticate(username=request.data['id'], password=request.data['password'])
        if user is not None:
            token = Token.objects.get(user=user)
            # return Response({"login": "로그인 성공"}, template_name='index.html')   #로그인 성공후 토큰을 가져온다.
            return Response({'token': token.key, "login": "로그인 성공"})  # 로그인 성공후 토큰을 가져온다.
        else:
            return Response(status=401) #로그인 실패


##토큰을 통해 정상적으로 데이터를 가져올 수 있는지 확인답
##토큰을 통해 정상적으로 API요청이 가능한지 test
class UserInfo(APIView):

    ###UserInfo API는 로그인한 사용자에게만 접근이 허용된다. 유효하지 않으면 401에러 응
    ###IsAuthenticated : 인증되지 않은 사용자에게 권한을 거부하고 인증된 사람만 허용한다.
    ##ALLowAny : 누구나 가능
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated]
    #JWT 인증을 확인하기 위해 사용한다
    authentication_classes = [JSONWebTokenAuthentication]

    def get(self, request, *args, **kwargs):
        username = request.query_params.get("username")
        query = User.objects.get(username=username)

        serializer = UserProfileSerializer(query, many=False)

        return Response(serializer.data["profile"])
