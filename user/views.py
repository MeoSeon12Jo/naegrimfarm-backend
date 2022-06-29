from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from django.contrib.auth import login, logout, authenticate
from user.serializers import UserSerializer
from user.jwt_claim_serializer import SpartaTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from user.models import User as UserModel

#회원 관련 view
class UserView(APIView):
    
    #TODO 회원정보 조회
    def get(self, request):
        user = request.user
        user_serializer = UserSerializer(user, context={"request": request})
        
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    
    #TODO 회원가입
    def post(self, request):
        user_serializer = UserSerializer(data=request.data, context={"request": request})
        
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    #TODO 회원정보 수정
    def put(self, request, id):
        user = UserModel.objects.get(id=id)
        user_serializer = UserSerializer(user, data=request.data, partial=True, context={"request": request})
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #TODO 회원탈퇴
    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "회원 탈퇴 완료!"})
    
    
class SpartaTokenObtainPairView(TokenObtainPairView):
    #serializer_class 변수에 커스터마이징 된 시리얼라이저를 넣어 준다!
    serializer_class = SpartaTokenObtainPairSerializer
    
#로그인/로그아웃 view
class UserApiView(APIView):
    
    #DONE 로그인
    def post(self, request):
        email = request.data.get('email', '')
        password = request.data.get('password', '')

        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({"error": "존재하지 않는 이메일이거나 패스워드가 일치하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        
        login(request, user)
        return Response({"msg": "로그인에 성공했습니다."}, status=status.HTTP_200_OK)
    
    #DONE 로그아웃
    def delete(self, request):
        logout(request)
        return Response({"msg": "로그아웃 되었습니다."}, status=status.HTTP_200_OK)
    
    
# 인가된 사용자만 접근할 수 있는 View 생성
class OnlyAuthenticatedUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
		
    # JWT 인증방식 클래스 지정하기
    authentication_classes = [JWTAuthentication]

    def get(self, request):
				# Token에서 인증된 user만 가져온다.
        user = request.user
        print(f"user 정보 : {user}")
        if not user:
            return Response({"error": "접근 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"message": "Accepted"})
