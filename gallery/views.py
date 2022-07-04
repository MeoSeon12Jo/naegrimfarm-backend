from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, PaintingSerializer
from auction.models import Painting as PaintingModel
from user.models import User as UserModel
from rest_framework import status
from django.db.models import Q
import cv2
import numpy as np

def transform(img, net):
    h, w, c = img.shape
    img = cv2.resize(img, dsize=(500, int(h / w * 500)))
    print(img.shape)

    MEAN_VALUE = [103.939, 116.779, 123.680]
    blob = cv2.dnn.blobFromImage(img, mean=MEAN_VALUE)

    print(blob.shape) # (1, 3, 325, 500)
    net.setInput(blob)
    output = net.forward()

    output = output.squeeze().transpose((1, 2, 0))
    output += MEAN_VALUE

    output = np.clip(output, 0, 255)
    output = output.astype('uint8')

    return output

class PaintingView(APIView):

    def post(self, request):
        user = request.user
        request.data["user"] = user.id
        painting_serializer = PaintingSerializer(data=request.data, context={"request": request})
        if painting_serializer.is_valid():
            painting_serializer['image']=transform(painting_serializer['image'], cv2.dnn.readNetFromTorch('composition_vii.t7'))
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