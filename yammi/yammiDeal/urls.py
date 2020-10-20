from django.urls import path
from .views import *

urlpatterns = [
    path('deal/', DealView.as_view(), name='deal'),
    path('deal/detail/', DetailDeal.as_view(), name='detail')
    # path('transactional_information/', LoginView.as_view(), name='transactional_information'),
    # path('get-user/', UserInfo.as_view()),
]