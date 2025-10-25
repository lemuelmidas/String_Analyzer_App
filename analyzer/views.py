from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import AnalyzedString
from .serializers import AnalyzedStringSerializer
from .utils import analyze_string

@api_view(['GET'])
def api_root(request):
    return Response({
        "message": "Welcome to the String Analyzer API 🚀",
        "endpoints": {
            "POST /strings/": "Analyze a new string",
            "GET /strings/<text_value>/": "Retrieve string details",
            "DELETE /strings/<text_value>/delete/": "Delete analyzed string",
            "GET /strings/filter-by-natural-language/": "Natural language filter"
        }
    })

@api_view(['POST'])
def create_analyzed_string(request):
    if 'text' not in request.data:
        return Response({'error': "Missing 'text' field"}, status=status.HTTP_400_BAD_REQUEST)

    text = request.data['text']
    if AnalyzedString.objects.filter(text=text).exists():
        return Response({'error': 'String already analyzed'}, status=status.HTTP_409_CONFLICT)

    analyzed_data = analyze_string(text)
    serializer = AnalyzedStringSerializer(data={**request.data, **analyzed_data})

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_single_string(request, text_value):
    try:
        analyzed = AnalyzedString.objects.get(text=text_value)
        serializer = AnalyzedStringSerializer(analyzed)
        return Response(serializer.data)
    except AnalyzedString.DoesNotExist:
        return Response({'error': 'String not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_analyzed_string(request, text_value):
    try:
        analyzed = AnalyzedString.objects.get(text=text_value)
        analyzed.delete()
        return Response({'message': 'Deleted successfully'}, status=status.HTTP_200_OK)
    except AnalyzedString.DoesNotExist:
        return Response({'error': 'String not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def filter_by_natural_language(request):
    query = request.GET.get('query', '').lower()
    queryset = AnalyzedString.objects.all()

    if 'palindrome' in query:
        queryset = queryset.filter(is_palindrome=True)
    if 'longer than' in query:
        try:
            num = int(query.split('longer than')[1].split()[0])
            queryset = queryset.filter(length__gt=num)
        except:
            pass
    if 'shorter than' in query:
        try:
            num = int(query.split('shorter than')[1].split()[0])
            queryset = queryset.filter(length__lt=num)
        except:
            pass

    serializer = AnalyzedStringSerializer(queryset, many=True)
    return Response(serializer.data)
