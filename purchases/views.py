from django.shortcuts import get_object_or_404

from rest_framework.views import APIView


# Create your views here.
class OrderView(APIView):
    def post(self, request):
        pass