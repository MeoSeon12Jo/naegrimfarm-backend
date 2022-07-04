from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, PaintingSerializer
from auction.models import Painting as PaintingModel
from user.models import User as UserModel
from rest_framework import permissions
from rest_framework import status
from django.db.models import Q


class PaintingView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = request.user
        request.data["user"] = user.id
        painting_serializer = PaintingSerializer(data=request.data, context={"request": request})
        if painting_serializer.is_valid():
            painting_serializer.save()
            return Response(painting_serializer.data, status=status.HTTP_200_OK)
        return Response(painting_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GalleryView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        users = UserModel.objects.filter(~Q(owner_painting=None))
        user_serializer = UserSerializer(users, many=True).data
        user_serializer.sort(key=lambda x: -len(x['paintings_list']))

        return Response(user_serializer, status=status.HTTP_200_OK)


class UserGalleryView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, nickname):
        user_id = UserModel.objects.get(nickname=nickname).id
        paintings = PaintingModel.objects.filter(owner=user_id, is_auction=False).order_by('-auction__current_bid')
        painting_serializer = PaintingSerializer(paintings, many=True).data

        return Response(painting_serializer, status=status.HTTP_200_OK)
    
# class MyGalleryView(APIView):
    
#     def get(self, request):
#         user = request.user.id
#         user_id = UserModel.objects.get(id=user).id
#         paintings = PaintingModel.objects.filter(owner=user_id, is_auction=False).order_by('-auction__current_bid')
#         painting_serializer = PaintingSerializer(paintings, many=True).data

#         return Response(painting_serializer, status=status.HTTP_200_OK)
