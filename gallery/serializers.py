from rest_framework import serializers
from user.models import User as UserModel
from auction.models import Category as CategoryModel
from auction.models import Painting as PaintingModel
from auction.models import Auction as AuctionModel


class PaintingSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaintingModel
        
        # fields = ["username", "email", "fullname", "join_date",
    #     "userprofile", "article_set"]
        fields = "__all__"