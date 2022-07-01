from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, PaintingSerializer
from auction.models import Painting as PaintingModel
from user.models import User as UserModel
from rest_framework import status
from django.db.models import Q


class GalleryView(APIView):
    
    def get(self, request):
        users = UserModel.objects.filter(~Q(owner_painting=None))
        user_serializer = UserSerializer(users, many=True).data

        return Response(user_serializer, status=status.HTTP_200_OK)


class UserGalleryView(APIView):

    def get(self, request, nickname):

        user_id = UserModel.objects.get(nickname=nickname).id
        paintings = PaintingModel.objects.filter(owner=user_id, is_auction=False).order_by('-auction__current_bid')
        painting_serializer = PaintingSerializer(paintings, many=True).data
        
        return Response(painting_serializer, status=status.HTTP_200_OK)
