#from rest_framework import generics
#from .models import AnalyzedString
#from .serializers import AnalyzedStringSerializer

#class StringListCreateView(generics.ListCreateAPIView):
#    queryset = AnalyzedString.objects.all()
#    serializer_class = AnalyzedStringSerializer

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

def home(request):
    return JsonResponse({"message": "String Analyzer API is running ✅ Use /strings/ to access the API."})

class AnalyzeStringView(APIView):
    def get(self, request):
        return Response({"message": "GET method works!"})

    def post(self, request):
        data = request.data
        text = data.get("text")
        if not text:
            return Response({"error": "Text field is required"}, status=status.HTTP_400_BAD_REQUEST)
        # Do your string analysis here...
        return Response({"text": text, "length": len(text)})
