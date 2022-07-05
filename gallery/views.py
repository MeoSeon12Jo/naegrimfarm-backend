from datetime import datetime
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, PaintingSerializer, PaintingUploadSerializer
from auction.models import Category as CategoryModel, Painting as PaintingModel
from auction.models import Auction as AuctionModel
from user.models import User as UserModel
from rest_framework import permissions
from rest_framework import status
from django.db.models import Q
import cv2
import numpy as np
import sys
import io
from PIL import Image
from django.utils import timezone
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms.models import model_to_dict
import random


def transform(img, net):
    #img를 boundfield로 읽는다.
    data = img.read()
    #인코딩
    encoded_img = np.fromstring(data, dtype = np.uint8)
    #다시 디코딩
    img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
    #어떤 모양인지 shape
    h, w, c = img.shape
    #500x500으로 크기조정
    img = cv2.resize(img, dsize=(500, int(h / w * 500)))
    #모델: 명화로 바꾸는 부분
    MEAN_VALUE = [103.939, 116.779, 123.680]
    blob = cv2.dnn.blobFromImage(img, mean=MEAN_VALUE)
    # print(blob.shape) # (1, 3, 325, 500)
    
    #어떤 명화로 바꿀지
    net.setInput(blob)
    output = net.forward()
    #아웃풋 크기 조정
    output = output.squeeze().transpose((1, 2, 0))
    output += MEAN_VALUE
    #크기에 맞게 자르고 type을 바꿔줌!
    output = np.clip(output, 0, 255)
    output = output.astype('uint8')
    
    output = Image.fromarray(output)
    output_io = io.BytesIO()
    output.save(output_io, format="JPEG")
    return output_io

class PaintingView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = request.user
        now = datetime.now()
        category = CategoryModel.objects.get(name=request.data["category"])
        model_list = ['gallery/composition_vii.t7', 'gallery/candy.t7', 'gallery/feathers.t7', 'gallery/la_muse.t7', 'gallery/masaic.t7', 'gallery/starry_night.t7', 'gallery/the_scream.t7', 'gallery/the_wave.t7', 'gallery/udnie.t7']
        random.shuffle(model_list)
        output_io = transform(request.data['image'], net=cv2.dnn.readNetFromTorch(model_list[0]))
        
        new_pic= InMemoryUploadedFile(output_io, 'ImageField',f"{user.nickname}:{now}",'JPEG', sys.getsizeof(output_io), None)
        
        create_paintings = PaintingModel.objects.create(
            title=request.data["title"],
            description=request.data["description"],
            artist=user,
            owner=user,
            category=category,
            image=new_pic,
        )
        
        painting_dict = model_to_dict(create_paintings)
        painting_dict['image'] = painting_dict['image'].url
        return Response(painting_dict, status=status.HTTP_200_OK)



class GalleryView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        user = request.user
        my_point = UserModel.objects.get(id=user.id).point

        closed_auctions = AuctionModel.objects.filter(Q(auction_end_date__lte=timezone.now()))

        for closed_auction in closed_auctions:
            if closed_auction.bidder:
                closed_auction.painting.owner_id = closed_auction.bidder_id
                closed_auction.painting.is_auction = False
                closed_auction.painting.save()

        users = UserModel.objects.filter(~Q(owner_painting=None) & Q(owner_painting__is_auction=False)).distinct()
        
        if users.count() != 0:
            user_serializer = UserSerializer(users, many=True).data
            user_serializer.sort(key=lambda x: -len(x['paintings_image']))

            return Response({'user_serializer': user_serializer, 'my_point': my_point}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class UserGalleryView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, nickname):
        user = request.user
        my_point = UserModel.objects.get(id=user.id).point

        user_id = UserModel.objects.get(nickname=nickname).id
        paintings = PaintingModel.objects.filter(owner=user_id, is_auction=False).order_by('-auction__current_bid')
        painting_serializer = PaintingSerializer(paintings, many=True).data

        return Response({'painting_serializer': painting_serializer, 'my_point': my_point}, status=status.HTTP_200_OK)