#from django.urls import path
#from .views import StringListCreateView

#urlpatterns = [
#    path('strings/', StringListCreateView.as_view(), name='string-list-create'),
#]


from django.urls import path
from .views import AnalyzeStringView, home

urlpatterns = [
    path('', home, name='home'),  # <-- home page
    path('strings/', AnalyzeStringView.as_view(), name='string-list-create'),
]


