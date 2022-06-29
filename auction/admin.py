from django.contrib import admin
from .models import Category as CategoryModel
from .models import Painting as PaintingModel
from .models import Auction as AuctionModel


admin.site.register(CategoryModel)
admin.site.register(PaintingModel)
admin.site.register(AuctionModel)