from django.urls import path
from .views import CalculateMultiYearGainView  # Import your view

app_name = 'portfolio_analyzer'

urlpatterns = [
    path('calculate_multi_year_gain/', CalculateMultiYearGainView.as_view(), name='calculate-multi-year-gain'),
    # ... other URL patterns ...
]
