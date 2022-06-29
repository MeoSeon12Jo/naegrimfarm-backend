from django.urls import path

from .views import UserView, UserApiView
from rest_framework_simplejwt.views import (
    TokenObtainPairView, #기본 JWT access 토큰 발급 view 인증토큰
    TokenRefreshView, # JWT refresh 토큰 발급 view 인증토큰을 재발급받기위한 또 다른 토큰 
)
from user.views import FarmTokenObtainPairView, OnlyAuthenticatedUserView


urlpatterns = [
    path('', UserView.as_view()),
    path('login/', UserApiView.as_view()),
    path('logout/', UserApiView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/farm/token/', FarmTokenObtainPairView.as_view(), name='sparta_token'),
    path('api/authonly/', OnlyAuthenticatedUserView.as_view()),
]