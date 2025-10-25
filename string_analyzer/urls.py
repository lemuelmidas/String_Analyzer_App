from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "message": "Welcome to the String Analyzer API!",
        "routes": {
            "POST /api/analyze/": "Analyze and store a string",
            "GET /api/strings/": "List all analyzed strings",
            "GET /api/strings/<text_value>/": "Get one string",
            "DELETE /api/strings/<text_value>/delete/": "Delete string",
            "GET /api/filter/": "Natural language filter"
        }
    })

urlpatterns = [
    path('', home, name='home'),  # 👈 handles root /
    path('admin/', admin.site.urls),
    path('api/', include('analyzer.urls')),
]
