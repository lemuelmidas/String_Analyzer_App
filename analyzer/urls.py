from django.urls import path
from . import views

urlpatterns = [
    path('analyze/', views.create_analyzed_string, name='create_analyzed_string'),
    path('strings/', views.get_all_strings, name='get_all_strings'),
    path('strings/<str:text_value>/', views.get_single_string, name='get_single_string'),
    path('strings/<str:text_value>/delete/', views.delete_analyzed_string, name='delete_analyzed_string'),
    path('filter/', views.filter_by_natural_language, name='filter_by_natural_language'),
]
