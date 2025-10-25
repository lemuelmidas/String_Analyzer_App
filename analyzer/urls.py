from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_root, name='api_root'),
    path('strings/', views.create_analyzed_string, name='create_analyzed_string'),
    path('strings/<str:text_value>/', views.get_single_string, name='get_single_string'),
    path('strings/filter-by-natural-language/', views.filter_by_natural_language, name='filter_by_natural_language'),
    path('strings/<str:text_value>/delete/', views.delete_analyzed_string, name='delete_analyzed_string'),
]
