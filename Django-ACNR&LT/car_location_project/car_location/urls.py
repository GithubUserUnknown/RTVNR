from django.urls import path
from .views import index, search_plate, car_location_history  # Import the new view

urlpatterns = [
    path('', index, name='index'),
    path('search/', search_plate, name='search_plate'),  # Existing search plate URL
    path('history/', car_location_history, name='car_location_history'),  # New URL pattern for history
]