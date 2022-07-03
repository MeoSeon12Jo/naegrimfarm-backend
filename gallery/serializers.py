from rest_framework import serializers
from user.models import User as UserModel
from auction.models import Category as CategoryModel
from auction.models import Painting as PaintingModel
from auction.models import Auction as AuctionModel


class PaintingDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    artist_name = serializers.SerializerMethodField()
    artist_paintings = serializers.SerializerMethodField()
    
    def get_category_name(self, obj):
        return obj.category.name
    
    def get_artist_name(self, obj):
        return obj.artist.nickname
    
    def get_artist_paintings(self, obj):
        paintings = PaintingModel.objects.filter(artist=obj.artist.id).values()
        
        painting_list = []
        for painting in paintings:
            if painting.get('is_auction') == True:
                painting_id = painting["id"]
                painting_image = painting["image"]
                
                painting_dict = {"painting_id" : painting_id, "painting_image": painting_image}
                
                painting_list.append(painting_dict)

        return painting_list

        
    class Meta:
        model = PaintingModel
        fields = ["id", "title", "description", "image",
        "is_auction","artist", "artist_name", "owner", 
        "category_name", "artist_paintings", "auction"]


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


class PaintingSerializer(serializers.ModelSerializer):
    artist = UserSerializer()
    owner = serializers.SerializerMethodField()
    auction = serializers.SerializerMethodField()

    def get_owner(self, obj):
        return obj.owner.nickname

    def get_auction(self, obj):
        auction = AuctionModel.objects.filter(painting=obj.id).values()

        return auction

    class Meta:
        model = PaintingModel
        fields = ["id", "title", "description", "image",
        "is_auction", "artist", "owner", "category", "auction"]