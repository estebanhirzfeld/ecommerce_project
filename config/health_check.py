"""
Health check endpoint for monitoring and deployment platforms.
"""
from django.http import JsonResponse
from django.db import connection
from django.conf import settings


def health_check(request):
    """
    Simple health check endpoint that verifies:
    - Application is running
    - Database connection is working
    """
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            'status': 'healthy',
            'debug': settings.DEBUG,
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e),
        }, status=503)
