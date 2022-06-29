from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PaintingSerializer
from auction.models import Painting as PaintingModel


class GalleryView(APIView):
    
    def get(self, request):
        paintings = PaintingModel.objects.filter(is_auction=False)
        painting_serializer = PaintingSerializer(paintings, many=True).data

        return Response(painting_serializer)
        