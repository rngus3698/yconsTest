from django.urls import path
from .views import *


urlpatterns = [
    path('deal/', DealView.as_view(), name='deal'),
    path('deal/detail/', DetailDeal.as_view(), name='detail'),

]