from django.urls import path

from .views import AuctionView, AuctionDetailView

urlpatterns = [
    path('', AuctionView.as_view(),),
    path('detail/<int:id>/', AuctionDetailView.as_view(),),

]