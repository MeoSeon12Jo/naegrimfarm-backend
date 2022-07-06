from rest_framework import serializers
from auction.models import Painting as PaintingModel
from auction.models import Auction as AuctionModel
from auction.models import BookMark as BookMarkModel
from django.forms.models import model_to_dict


class BookmarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookMarkModel
        fields = "__all__"


class PaintingSerializer(serializers.ModelSerializer):

    auction = serializers.SerializerMethodField()

    def get_auction(self, obj):
        if obj.is_auction == True:
            auction = model_to_dict(obj.auction)
            return auction

    class Meta:
        model = PaintingModel
        fields = ["id", "artist", "image", "is_auction", "owner", "title", "auction"]


class AucionSerializer(serializers.ModelSerializer):
    
    bidder = serializers.SerializerMethodField()
    painting = PaintingSerializer()
    auction_end_date = serializers.SerializerMethodField()

    def get_bidder(self, obj):
        bidder = obj.bidder.nickname
        return bidder

    # 시간을 js에서 활용가능한 규칙으로 바꿈
    def get_auction_end_date(self, obj):
        auction_end_date = obj.auction_end_date.replace(microsecond=0).isoformat()
        return auction_end_date

    class Meta:
        model = AuctionModel
        fields = ["id", "current_bid", "bidder", "auction_end_date", "painting"]