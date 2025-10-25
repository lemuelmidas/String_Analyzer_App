from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import AnalyzedString
from .serializers import AnalyzedStringSerializer
from .utils import analyze_string


@api_view(['POST'])
def create_analyzed_string(request):
    """
    Create and analyze a new string.
    """
    if 'text' not in request.data:
        return Response({'error': "Missing 'text' field"}, status=status.HTTP_400_BAD_REQUEST)

    text = request.data['text']

    # Prevent duplicates
    if AnalyzedString.objects.filter(text=text).exists():
        return Response({'error': 'String already analyzed'}, status=status.HTTP_409_CONFLICT)

    analyzed_data = analyze_string(text)
    serializer = AnalyzedStringSerializer(data={**request.data, **analyzed_data})

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_all_strings(request):
    """
    Retrieve all analyzed strings with optional filters.
    """
    queryset = AnalyzedString.objects.all()

    # Optional filters
    min_length = request.GET.get('min_length')
    max_length = request.GET.get('max_length')
    is_palindrome = request.GET.get('is_palindrome')

    if min_length:
        queryset = queryset.filter(length__gte=int(min_length))
    if max_length:
        queryset = queryset.filter(length__lte=int(max_length))
    if is_palindrome is not None:
        queryset = queryset.filter(is_palindrome=(is_palindrome.lower() == 'true'))

    serializer = AnalyzedStringSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_single_string(request, text_value):
    """
    Retrieve a single analyzed string by its text value.
    """
    try:
        analyzed = AnalyzedString.objects.get(text=text_value)
        serializer = AnalyzedStringSerializer(analyzed)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except AnalyzedString.DoesNotExist:
        return Response({'error': 'String not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_analyzed_string(request, text_value):
    """
    Delete an analyzed string by its text value.
    """
    try:
        analyzed = AnalyzedString.objects.get(text=text_value)
        analyzed.delete()
        return Response({'message': 'Deleted successfully'}, status=status.HTTP_200_OK)
    except AnalyzedString.DoesNotExist:
        return Response({'error': 'String not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def filter_by_natural_language(request):
    """
    Filter analyzed strings based on a natural language query.
    Example: ?query=palindromes longer than 5 characters
    """
    query = request.GET.get('query', '').lower()
    queryset = AnalyzedString.objects.all()

    if 'palindrome' in query:
        queryset = queryset.filter(is_palindrome=True)
    if 'longer than' in query:
        try:
            number = int(query.split('longer than')[1].split()[0])
            queryset = queryset.filter(length__gt=number)
        except (ValueError, IndexError):
            pass
    if 'shorter than' in query:
        try:
            number = int(query.split('shorter than')[1].split()[0])
            queryset = queryset.filter(length__lt=number)
        except (ValueError, IndexError):
            pass

    serializer = AnalyzedStringSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
