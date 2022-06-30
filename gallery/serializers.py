from rest_framework import serializers
from user.models import User as UserModel
from auction.models import Category as CategoryModel
from auction.models import Painting as PaintingModel
from auction.models import Auction as AuctionModel


class PaintingSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaintingModel
        # fields = ["id", "title", "description", "image",
        # "is_auction", "artist", "owner", "category"]
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    
    paintings_list = serializers.SerializerMethodField()

    def get_paintings_list(self, obj):
        paintings_set = PaintingModel.objects.filter(owner=obj.id).values()
        paintings_list = []
        for paintings in paintings_set:
            if paintings.get('is_auction') == False:
                paintings_list.append(paintings)
        return paintings_list

    class Meta:
        model = UserModel
        fields = ["id", "email", "nickname", "point", "paintings_list"]
        # fields = "__all__"