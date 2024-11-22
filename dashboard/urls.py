from django.urls import path
from . import views

urlpatterns = [
    path('chart-data/', views.chart_data, name='chart_data'),
    path('', views.index, name='dashboard-index'),  # Default view for dashboard
    path('reports', views.reports, name="dashboard-reports"),
    path('get-filtered-data/', views.get_filtered_data, name='get_filtered_data'),
]