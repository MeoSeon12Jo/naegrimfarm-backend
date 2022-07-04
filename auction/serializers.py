
from django.forms import ValidationError
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from gallery.serializers import PaintingSerializer
from gallery.serializers import PaintingDetailSerializer
from auction.models import Auction as AuctionModel
from auction.models import AuctionComment as AuctionCommentModel
from auction.models import BookMark as BookMarkModel

from django.utils import timezone
from datetime import datetime, timedelta


class AuctionSerializer(serializers.ModelSerializer):
    painting = PaintingSerializer()
    auction_end_date = serializers.SerializerMethodField()
    start_bid = serializers.SerializerMethodField()
    current_bid = serializers.SerializerMethodField()

    # 마감까지 남은 시간 포맷팅
    def get_auction_end_date(self, obj):
        time_remaining = obj.auction_end_date - timezone.now()
        time_remaining = str(timedelta(seconds=time_remaining.seconds))
        time_list = time_remaining.split(":")
        time_list.insert(1, "시간")
        time_list.insert(3, "분")
        time_list.insert(5, "초")
        time_list = time_list[:4]
        return ' '.join(time_list)
    
    # 입찰가 포맷팅
    def get_start_bid(self, obj):
        return format(obj.start_bid, ',')

    def get_current_bid(self, obj):
        return format(int(obj.current_bid or 0), ',') # start_bid=None 이면 int값으로 변환

    def create(self, validated_data):
        auction = AuctionCommentModel(**validated_data)
        auction.save()
        return auction

    class Meta:
        model = AuctionModel
        fields = ['id', 'start_bid', 'current_bid', 'auction_start_date', 
                        'auction_end_date', 'bidder', 'painting']
    
    
class AuctionCommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    create_time = serializers.SerializerMethodField()
    
    def get_username(self, obj):
        return obj.user.nickname
    
    def get_create_time(self, obj):
        #JS에서 댓글 시간 표현방식 사용하기 위해 포멧
        create_time = obj.created_at.replace(microsecond=0).isoformat()
        return create_time
    
    def create(self, validated_data):
        comment = AuctionCommentModel(**validated_data)
        comment.save()
        
        return comment
    
    def update(self, instance, validated_data):
        
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        
        return instance
    
    class Meta:
        model = AuctionCommentModel
        fields = ["id","user", "auction", "username", "content", "created_at", "create_time"]

    
class AuctionDetailSerializer(serializers.ModelSerializer):
    painting = PaintingDetailSerializer()
    comments = AuctionCommentSerializer(many=True, source="auctioncomment_set")
    start_bid = serializers.SerializerMethodField()
    current_bid = serializers.SerializerMethodField()
    time_left = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
    is_bookmark = serializers.SerializerMethodField()
    request_username = serializers.SerializerMethodField()
    
    def get_start_bid(self, obj):
        #포맷 메소드로 숫자를 , 로 분리!
        return format(obj.start_bid, ',')
    
    def get_current_bid(self, obj):
        return format(int(obj.current_bid or 0), ',')
    

    def get_time_left(self, obj):
        #timedelta형식의 시간을 원하는 형태로 바꾸는 로직
        
        time_remaining = obj.auction_end_date - timezone.now()
        time_string = str(time_remaining)
        
        if 'days' not in time_string:
            time_string = '0 days, ' + time_string
        
        time_string = time_string.split(",")
        
        days = time_string[0]
        days = days[:-5]
        
        times = time_string[1]
        times = times[1:]
        times = times.split(":")
        
        hours = times[0]
        minutes = times[1]
        
        time_remaining = f"{days}일 {hours}시간 {minutes}분"
        
        return time_remaining
    
    def get_end_date(self, obj):
        #datetime 을 JS에서 Date()메소드에서 사용 할 수 있는 형태로 변경
        end_time = str(obj.auction_end_date)
        time_list = end_time.split("+")[0]
        end_date = time_list.split(" ")[1]
  
        
        return end_date
    
    def get_is_bookmark(self, obj):
        user = self.context.get("request").user
        try:
            BookMarkModel.objects.get(user_id=user.id, auction_id=obj.id)
            return True
        except BookMarkModel.DoesNotExist:
            return False
        
    def get_request_username(self, obj):
        user = self.context.get("request").user
        return user.nickname
     
    class Meta:
        model = AuctionModel
        fields = ["id","request_username", "start_bid", "current_bid", "time_left",
                  "end_date", "bidder", "comments", "painting", "is_bookmark"]
    
        
class AuctionBidSerializer(serializers.ModelSerializer):
    current_bid_format = serializers.SerializerMethodField()
    
    def get_current_bid_format(self, obj):
        return format(obj.current_bid, ',')
    
    
    def validate(self, data):
        http_method = self.context.get("request").method
        user = self.context.get("request").user
        bidder = self.instance.bidder
        
        bid_price = data.get("current_bid")
        current_bid = self.instance.current_bid
        start_bid = self.instance.start_bid
        
        #입찰시 validation
        if http_method == "PUT":
            if bid_price%100000 != 0:
                raise serializers.ValidationError(
                    detail={"error": "10만 포인트 단위로 입찰해주세요."}
                )
            if bid_price < start_bid:
                raise serializers.ValidationError(
                    detail={"error": "시작 입찰가보다 적은 금액으로 입찰 하실 수 없습니다."}
                )
            elif bid_price <= int(current_bid or 0):
                raise serializers.ValidationError(
                    detail={"error": "현재 입찰가보다 같거나 적은 금액으로 입찰 하실 수 없습니다."}
                )
            elif user.point < bid_price:
                raise serializers.ValidationError(
                    detail={"error": f"포인트가 부족합니다. 현재 보유중인 포인트는 {user.point} 입니다. 입찰가를 확인 해주세요."}
                )
            elif user == bidder:
                raise serializers.ValidationError(
                    detail={"error": "현재 이미 최고가로 입찰중입니다."}
                )
            
        return data
    
    def update(self, instance, validated_data):
        user = self.context.get("request").user
        bidder = instance.bidder
        
        if bidder is not None:
            bidder.point = bidder.point + instance.current_bid
            bidder.save()
            
        for key, value in validated_data.items():
            setattr(instance, key, value)
        
        user.point = user.point - instance.current_bid
        user.save()
        
        instance.bidder_id = user.id
        instance.save()
        
        return instance
    
    class Meta:
        model = AuctionModel
        fields = ["id","current_bid", "bidder", "current_bid_format"]
        
