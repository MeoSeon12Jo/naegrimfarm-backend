from email.policy import HTTP
from rest_framework.views import APIView
from rest_framework.response import Response
from auction.models import BookMark as BookMarkModel
from auction.models import Auction as AuctionModel
from auction.models import Painting as PaintingModel
from .serializers import AucionSerializer, PaintingSerializer
from rest_framework import status
from django.db.models import Q


class MyPageView(APIView):

    def get(self, request, nickname):
        bookmarks = BookMarkModel.objects.filter(user=request.user.id).values()
        paintings = PaintingModel.objects.filter(owner=request.user.id).order_by('-auction__current_bid')
        auctions = AuctionModel.objects.filter(bidder=request.user.id).order_by('auction_end_date')

        paintings_serializer = PaintingSerializer(paintings, many=True).data
        auctions_serializer = AucionSerializer(auctions, many=True).data
        
        return Response(
            {
                'paintings_serializer': paintings_serializer,
                'auctions_serializer': auctions_serializer,
                'bookmarks': bookmarks
            }
            , status=status.HTTP_200_OK
        )