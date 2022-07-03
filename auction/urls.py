from django.urls import path

from .views import AuctionView, AuctionDetailView, AuctionCommentView, BookMarkView

urlpatterns = [
    #/auction/
    path('', AuctionView.as_view(),),
    path('detail/<int:id>/', AuctionDetailView.as_view(),),
    path('detail/comment/<int:id>/', AuctionCommentView.as_view(),),
    path('detail/bookmark/<int:id>/', BookMarkView.as_view(),),
]