from django.urls import path
from .api import TripListCreateView, TripRetrieveUpdateDestroyView

urlpatterns = [
    path('trips/', TripListCreateView.as_view(), name='trip-list-create'),
    path('trips/<int:pk>/', TripRetrieveUpdateDestroyView.as_view(), name='trip-detail'),
]
