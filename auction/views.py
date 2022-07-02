from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status

from auction.serializers import AuctionCommentSerializer, AuctionDetailSerializer
from auction.serializers import AuctionSerializer
from auction.serializers import AuctionBidSerializer
from auction.models import Auction as AuctionModel
from auction.models import AuctionComment as AuctionCommentModel
from auction.models import BookMark as BookMarkModel

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
        
        return Response({"error" : "옥션 마감 날짜가 지나서 조회가 불가능합니다."}, status=status.HTTP_400_BAD_REQUEST)
    
    #DONE 경매상세페이지 입찰
    def put(self, request, id):
        auction = AuctionModel.objects.get(id=id)       
        auction_serializer = AuctionBidSerializer(auction, data=request.data, context={"request": request})
        
        if auction_serializer.is_valid():
            auction_serializer.save()
            
            return Response(auction_serializer.data, status=status.HTTP_200_OK)
    
        return Response(auction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AuctionCommentView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [JWTAuthentication]
    
    #TODO 댓글작성
    def post(self, request, id):
        user = request.user
        request.data["user"] = user.id
        auction = AuctionModel.objects.get(id=id)
        request.data["auction"] = auction.id
        comment_serializer = AuctionCommentSerializer(data=request.data, context={"request": request})
        if comment_serializer.is_valid():
            comment_serializer.save()
            
            return Response(comment_serializer.data, status=status.HTTP_200_OK)
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #TODO 댓글수정
    def put(self, request, id):
        user = request.user.id
        request.data["user"] = user
        auction = AuctionModel.objects.get(id=id)
        comment_serializer = AuctionCommentSerializer(auction, data=request.data, context={"request": request})
        
        if comment_serializer.is_valid():
            comment_serializer.save()
            
            return Response(comment_serializer.data, status=status.HTTP_200_OK)
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #TODO 댓글삭제
    def delete(self, request, id):
        user = request.user
        comment = AuctionCommentModel.objects.get(id=id)
        if comment.user_id == user.id:
            comment.delete()
            return Response({"msg": "댓글이 삭제 되었습니다."}, status=status.HTTP_200_OK)
        
        return Response({"msg": "자신의 댓글만 삭제 가능합니다."}, status=status.HTTP_400_BAD_REQUEST)
    
    
class BookMarkView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [JWTAuthentication]
    
    #TODO 북마크추가/삭제
    def post(self, request, id):
        user = request.user.id
        auction = AuctionModel.objects.get(id=id)
        
        try:
            my_bookmark = BookMarkModel.objects.get(user_id=user, auction_id=auction.id)
            my_bookmark.delete()
        except BookMarkModel.DoesNotExist:
            my_bookmark = BookMarkModel(user_id=user, auction_id=auction.id)
            my_bookmark.save()
            
            return Response({"msg": "북마크에 저장되었습니다."})
        return Response({"msg": "북마크에서 삭제 되었습니다."})
        

