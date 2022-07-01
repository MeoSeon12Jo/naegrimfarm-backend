from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status

from auction.serializers import AuctionDetailSerializer
from auction.serializers import AuctionSerializer
from auction.serializers import AuctionBidSerializer
from auction.models import Auction as AuctionModel

from django.db.models import Q

from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework_simplejwt.authentication import JWTAuthentication

class AuctionView(APIView):
    def get(self, request):
        # 카테고리명 Query Parameter로 가져오기
        category_name = request.GET.get('category', None)

        # 마감하지 않은 경매들 모두 가져오기
        open_auctions =  AuctionModel.objects.filter(Q(auction_end_date__gt=timezone.now()))
      
        # 마감임박 경매 쿼리(마감 시간 < 1일)
        closing_query = Q(auction_end_date__lt=timezone.now()+timedelta(days=1))

        # 입찰 전 경매 쿼리
        nobid_query = (Q(current_bid=None) & Q(bidder=None))

        closing_auctions = open_auctions.filter(closing_query).order_by('auction_end_date')
        hot_auctions = open_auctions.order_by('-current_bid')
        nobid_auctions = open_auctions.filter(nobid_query)

        # 카테고리 버튼 누를시 카테고리 쿼리 추가
        if category_name:
            category_query = Q(painting__category__name=category_name)
            closing_query = closing_query.add((category_query), closing_query.AND)
            nobid_query = nobid_query.add((category_query), nobid_query.AND)
            
            closing_auctions = open_auctions.filter(closing_query).order_by('auction_end_date')
            hot_auctions = open_auctions.filter(category_query).order_by('-current_bid')
            nobid_auctions = open_auctions.filter(nobid_query)

        # 딕셔너리에 시이럴라이저화된 데이터 담아주기    
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
    
    # permission_classes = [permissions.IsAuthenticated]
    
    # authentication_classes = [JWTAuthentication]
    
    #DONE 경매상세페이지 정보
    def get(self, request, id):
        auction = AuctionModel.objects.get(id=id)
        
        if auction.auction_end_date > timezone.now():
            #마감날짜가 지나지 않았다면 데이터 전송
            auction_serializer = AuctionDetailSerializer(auction)
        
            return Response(auction_serializer.data, status=status.HTTP_200_OK)
        
        return Response({"msg" : "옥션 마감 날짜가 지나서 조회가 불가능합니다."}, status=status.HTTP_400_BAD_REQUEST)
    
    #DONE 경매상세페이지 입찰
    def put(self, request, id):
        """
        입찰기능, 인풋창 가격 입력받아서, 포인트차감,ok
        auction current_bid에 가격 저장ok
        기존입찰자(bidder)에게 포인트 반환ok
        없다면 그대로 저장, bidder 교체ok
        validation 입찰 받은 가격이 current_bid보다 작다면 
        return 현재가보다 적은금액으로 입찰 하실 수 없습니다.ok
        """
        auction = AuctionModel.objects.get(id=id)
        
        auction_serializer = AuctionBidSerializer(auction, data=request.data, context={"request": request})
        
        if auction_serializer.is_valid():
            auction_serializer.save()
            
            return Response({"msg": "입찰 성공!"}, status=status.HTTP_200_OK)
        
        return Response(auction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    
        
                
        return Response({"message": "Put 메소드임"})