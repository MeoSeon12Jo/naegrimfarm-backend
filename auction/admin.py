from django.contrib import admin
from .models import Category as CategoryModel
from .models import Painting as PaintingModel
from .models import Auction as AuctionModel
from .models import AuctionComment as AuctionCommentModel
from .models import BookMark as BookMarkModel


admin.site.register(CategoryModel)
admin.site.register(PaintingModel)
admin.site.register(AuctionModel)
admin.site.register(AuctionCommentModel)
admin.site.register(BookMarkModel)