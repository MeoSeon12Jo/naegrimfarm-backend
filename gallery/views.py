from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, PaintingSerializer
from auction.models import Painting as PaintingModel
from auction.models import Auction as AuctionModel
from user.models import User as UserModel
from rest_framework import permissions
from rest_framework import status
from django.db.models import Q
import cv2
import numpy as np
from django.utils import timezone


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
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

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
    permission_classes = [permissions.AllowAny]

    def get(self, request):
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

            return Response(user_serializer, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class UserGalleryView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, nickname):

        user_id = UserModel.objects.get(nickname=nickname).id
        paintings = PaintingModel.objects.filter(owner=user_id, is_auction=False).order_by('-auction__current_bid')
        painting_serializer = PaintingSerializer(paintings, many=True).data

        return Response(painting_serializer, status=status.HTTP_200_OK)