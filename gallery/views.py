from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from auction.models import Painting as PaintingModel
from user.models import User as UserModel
from rest_framework import status


class GalleryView(APIView):
    
    def get(self, request):
        users = UserModel.objects.all()
        user_serizlizer = UserSerializer(users, many=True).data

        return Response(user_serizlizer, status=status.HTTP_200_OK)
