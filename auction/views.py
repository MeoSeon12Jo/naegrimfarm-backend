from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status

from auction.serializers import AuctionDetailSerializer
from auction.serializers import AuctionSerializer
from auction.models import Auction as AuctionModel

from django.db.models import Q

from django.utils import timezone
from datetime import datetime, timedelta

class AuctionView(APIView):
    def get(self, request):
        # 카테고리명 Query Parameter로 가져오기
        category_name = request.GET.get('category', None)
      
        # 마감임박 경매 쿼리(마감 시간 < 1일)
        closing_query = Q(auction_end_date__gt=timezone.now()) & Q(auction_end_date__lt=timezone.now()+timedelta(days=1))
        closing_auctions = AuctionModel.objects.filter(closing_query).order_by('auction_end_date')

        # 인기 경매 쿼리
        hot_auctions = AuctionModel.objects.all().order_by('-current_bid')
    
        # 입찰 전 경매 쿼리
        nobid_query = (Q(current_bid=None) | Q(bidder=None))
        nobid_auctions = AuctionModel.objects.filter(nobid_query)

        # 카테고리 버튼 누를시 카테고리 쿼리 추가
        if category_name:
            category_query = Q(painting__category__name=category_name)
            closing_query = closing_query.add((category_query), closing_query.AND)
            nobid_query = nobid_query.add((category_query), nobid_query.AND)
            
            closing_auctions = AuctionModel.objects.filter(closing_query).order_by('auction_end_date')
            hot_auctions = AuctionModel.objects.filter(category_query).order_by('-current_bid')
            nobid_auctions = AuctionModel.objects.filter(nobid_query)

        # 딕셔너리에 시이럴라이저 3개 담아주기    
        closing_auction_serializer = AuctionSerializer(closing_auctions, many=True, context={"request": request}).data
        hot_auction_serializer = AuctionSerializer(hot_auctions, many=True, context={"request": request}).data
        nobid_auction_serializer = AuctionSerializer(nobid_auctions, many=True, context={"request": request}).data

        auctions = {
            'closing_auctions': closing_auction_serializer,
            'hot_auctions': hot_auction_serializer,
            'nobid_auctions': nobid_auction_serializer
        }

        return Response(auctions, status=status.HTTP_200_OK)

    
    #TODO 경매 추가
    def post(self, request):
        pass
        # user_serializer = UserSerializer(data=request.data, context={"request": request})
        
        # if user_serializer.is_valid():
        #     user_serializer.save()
        #     return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        # return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    #TODO 경매 수정
    def put(self, request, id):
        pass

        # user = UserModel.objects.get(id=id)
        # user_serializer = UserSerializer(user, data=request.data, partial=True, context={"request": request})
        # if user_serializer.is_valid():
        #     user_serializer.save()
        #     return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        # return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #TODO 경매 삭제
    def delete(self, request):
        pass
        # user = request.user
        # user.delete()
        # return Response({"message": "경매 삭제 완료!"})
    
    

class AuctionDetailView(APIView):
    
    #TODO 경매상세페이지 정보
    def get(self, request, id):
        """
        이미지ok, 카테고리ok, 제목ok, 작품설명ok, 남은시간??, 마감날짜ok, 시작가격ok, 현재가격ok
        artist의 닉네임ok, artist의 다른작품3가지ok, 
        댓글(유저이름ok, 댓글내용ok, 언제달렸는지(몇분전)시간만 가져와짐.)
        
        """
        auction = AuctionModel.objects.get(id=id)
        auction_serializer = AuctionDetailSerializer(auction).data
        
        return Response(auction_serializer, status=status.HTTP_200_OK)
    
    #TODO 경매상세페이지 입찰
    def post(self, request, id):
        """
        입찰기능, 인풋창 가격 입력받아서, 포인트차감, 
        auction current_bid에 가격 저장
        기존입찰자(bidder)에게 포인트 반환
        없다면 그대로 저장, bidder 교체
        validation 입찰 받은 가격이 current_bid보다 작다면 
        return 현재가보다 적은금액으로 입찰 하실 수 없습니다.
        """
        
        return Response()