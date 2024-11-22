from django.shortcuts import render
from django.http import JsonResponse
from .models import WXData
from django.utils.timezone import now, timedelta
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt



def chart_data(request):
    # Define the fixed start and end dates
    start_date = datetime(2024, 10, 14, 0, 0, 0)
    end_date = datetime(2024, 11, 12, 0, 0, 0)

    # Get the site_name from the request
    site_name = request.GET.get('site_name', None)

    # Filter data based on site_name and timestamp
    queryset = WXData.objects.filter(
        timestamp__gte=start_date,
        timestamp__lte=end_date,
        site_info=site_name  # Match the site name
    ).order_by('timestamp')

    # Prepare data for the chart
    chart_data = {
        "labels": [data.timestamp.strftime("%Y-%m-%d %H:%M:%S") for data in queryset],  # X-axis (timestamps)
        "datasets": [
            {
                "label": "Water Level (Avg)",
                "data": [data.lvl_ft_avg for data in queryset],
                "backgroundColor": "rgba(75, 192, 192, 0.2)",
                "borderColor": "rgba(75, 192, 192, 1)",
                "borderWidth": 2,
                "pointRadius": 0,
                "tension": 0,
            },
            {
                "label": "Conductivity (Avg)",
                "data": [data.cond_avg for data in queryset],
                "backgroundColor": "rgba(255, 159, 64, 0.2)",
                "borderColor": "rgba(255, 159, 64, 1)",
                "borderWidth": 2,
                "pointRadius": 0,
                "tension": 0,
            },
            {
                "label": "T (Avg)",
                "data": [data.t_avg for data in queryset],
                "backgroundColor": "rgba(54, 162, 235, 0.2)",
                "borderColor": "rgba(54, 162, 235, 1)",
                "borderWidth": 2,
                "pointRadius": 3,
                "tension": 0,
                "yAxisID": "yRight",
            },
        ],
    }

    # Return JSON response
    return JsonResponse(chart_data)


@csrf_exempt
def get_filtered_data(request):
    try:
        # Extract query parameters
        site_name = request.GET.get('site_name')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        # Validate and convert dates
        if start_date:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        # Query the WXData model with correct field names
        data = WXData.objects.filter(
            site_info=site_name,  # Correct field name
            timestamp__date__gte=start_date,  # Correct field name
            timestamp__date__lte=end_date  # Correct field name
        ).values('site_info', 'timestamp', 'lvl_ft_avg', 'cond_avg', 't_avg')  # Correct field names

        # Convert queryset to list
        data_list = list(data)

        # Return JSON response
        return JsonResponse(data_list, safe=False)

    except Exception as e:
        print(f"Error: {str(e)}")  # Optional: for debugging
        return JsonResponse({'error': str(e)}, status=500)

# Render dashboard view
def index(request):
    return render(request, "dashboard.html")

# Render reports view
def reports(request):
    return render(request, 'reports.html')
