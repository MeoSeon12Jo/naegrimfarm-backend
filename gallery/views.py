from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class GalleryView(APIView):
    
    def get(self, request):
        
        return Response({'msg': 'get 요청 받았습니다'})