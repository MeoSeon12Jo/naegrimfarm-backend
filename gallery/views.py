from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, PaintingSerializer
from auction.models import Painting as PaintingModel
from auction.models import Auction as AuctionModel
from user.models import User as UserModel
from rest_framework import permissions
from rest_framework import status
from django.db.models import Q

from django.utils import timezone


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
        closed_auctions = AuctionModel.objects.filter(Q(auction_end_date__lte=timezone.now()))

        for closed_auction in closed_auctions:
            if closed_auction.bidder:
                closed_auction.painting.owner_id = closed_auction.bidder_id
                closed_auction.painting.is_auction = False
                closed_auction.painting.save()

        users = UserModel.objects.filter(~Q(owner_painting=None))
        if users.count() != 0:
            user_serializer = UserSerializer(users, many=True).data
            user_serializer.sort(key=lambda x: -len(x['paintings_list']))

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

