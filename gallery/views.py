from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, PaintingSerializer
from auction.models import Painting as PaintingModel
from user.models import User as UserModel
from rest_framework import status
from django.db.models import Q
from deep_learning_with_images.main import Transform

Transform('D:\naegrimfarm-backend\naegrimfarm-backend\gallery\CD 명함사이즈.jpg')

class PaintingView(APIView):

    def post(self, request):
        user = request.user
        request.data["user"] = user.id
        painting_serializer = PaintingSerializer(data=request.data, context={"request": request})
        if painting_serializer.is_valid():
            painting_serializer['image']=Transform(painting_serializer['image'])
            print(painting_serializer)
            painting_serializer.save()
            return Response(painting_serializer.data, status=status.HTTP_200_OK)
        return Response(painting_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GalleryView(APIView):

    def get(self, request):
        users = UserModel.objects.filter(~Q(owner_painting=None))
        user_serializer = UserSerializer(users, many=True).data
        user_serializer.sort(key=lambda x: -len(x['paintings_list']))

        return Response(user_serializer, status=status.HTTP_200_OK)


class UserGalleryView(APIView):

    def get(self, request, nickname):
        user_id = UserModel.objects.get(nickname=nickname).id
        paintings = PaintingModel.objects.filter(owner=user_id, is_auction=False).order_by('-auction__current_bid')
        painting_serializer = PaintingSerializer(paintings, many=True).data

        return Response(painting_serializer, status=status.HTTP_200_OK)
