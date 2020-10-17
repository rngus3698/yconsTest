from django.urls import path
from .views import *
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('get-user/', UserInfo.as_view()),

    path('api-jwt-auth/', obtain_jwt_token),    #토큰 발급(로그인)
    path('api-jwt-auth/refresh/', refresh_jwt_token),   #토큰 갱신
    path('api-jwt-auth/verify/', verify_jwt_token),     #토큰 유효성 검사
]