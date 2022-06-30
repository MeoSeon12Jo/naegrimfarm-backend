from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from auction.models import Painting as PaintingModel
from auction.models import Auction as AuctionModel

# class CommentSerializer(serializers.ModelSerializer):
#     author = serializers.SerializerMethodField()

#     def get_author(self, obj):
#         return obj.author.fullname

#     class Meta:
#         model = Comment
#         fields = ("author", "content")


class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionModel
        fields = "__all__"



# class AuctionSerializer(serializers.ModelSerializer):
    # categories = serializers.ListField(required=False) # 프론트에서 list형식으로 데이터를 보내줄때 사용
    # comments = CommentSerializer(many=True, read_only=True, source="comment_set")
    
    # def validate(self, data):
    #     # categories = data.get('categories', [])
    #     categories = self.context.get('categories', [])
    #     category_list = []
    #     for category in categories:
    #         try:
    #             category_instance = Category.objects.get(category=category)
    #             category_list.append(category_instance)
    #         except Category.DoesNotExist:
    #             return Response({'message': "Please select a valid category."}, status=status.HTTP_400_BAD_REQUEST)
        
    #     data['categories'] = category_list
        
    #     return data

    # def create(self, validated_data):
    #     categories = validated_data.pop('categories')
    #     article = Article(**validated_data)
    #     article.save()
    #     article.category.add(*categories)

    #     return article

    # def update(self, instance, validated_data):
    #     # cannot assign many-to-many field directly
    #     categories = validated_data.pop('categories')

    #     for key, value in validated_data.items():
    #         setattr(instance, key, value)
        
    #     instance.save()
    #     instance.category.add(*categories)
        
    #     return instance


    # class Meta:
    #     model = Auction
    #     fields = ("artist", "start_bid", "current_bid", "category", "")
