from zlib import DEF_BUF_SIZE
from django.db import models
from user.models import User as UserModel

class Category(models.Model):
    name = models.CharField("이름", max_length=5)

    class Meta:
        db_table = "categories"

    def __str__(self):
        return f"[카테고리] id: {self.id} / 이름: {self.name}"


class Painting(models.Model):
    artist = models.ForeignKey(UserModel, verbose_name="원작자", on_delete=models.SET_NULL, null=True, related_name='artist_painting')
    owner = models.ForeignKey(UserModel, verbose_name="소유자", on_delete=models.CASCADE, related_name='owner_painting')
    title = models.CharField("제목", max_length=50)
    description = models.TextField("설명", max_length=256)
    category = models.ForeignKey(Category, verbose_name="카테고리", on_delete=models.SET_NULL, null=True)
    image = models.FileField("이미지", upload_to='paintings/')
    is_auction = models.BooleanField("경매상태", default=True)
    
    class Meta:
        db_table = "paintings"

    def __str__(self):
        return f"[작품] id: {self.id} / 제목: {self.title} / 소유자: {self.owner.nickname}"

class Auction(models.Model):
    start_bid = models.PositiveIntegerField("시작 입찰가")
    current_bid = models.PositiveIntegerField("현재 입찰가", blank=True, null=True)
    auction_start_date = models.DateTimeField("경매 시작일", auto_now_add=True)
    auction_end_date = models.DateTimeField("경매 종료일")
    painting = models.ForeignKey(Painting, on_delete=models.CASCADE)
    bidder = models.ForeignKey(UserModel, blank=True, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "auctions"

    def __str__(self):
        return f"[경매] id: {self.id} / 작품: {self.painting.title}"
    
    
class AuctionComment(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "auction_comments"
        
    def __str__(self):
        return f"[경매댓글] 경매id: {self.auction} / 작성자: {self.user}"
    
    
class BookMark(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "bookmarks"
    
    def __str__(self):
        return f"[북마크] 유저: {self.user.nickname} / 옥션id: {self.auction}"