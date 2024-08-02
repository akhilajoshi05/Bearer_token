# myapp/middleware.py
# from django.http import JsonResponse
# from student.models import APIKey

# class APIKeyMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.path == '/generate-api-key/':
#             return self.get_response(request)

#         api_key = request.headers.get('API-Key')
#         if not api_key or not APIKey.objects.filter(key=api_key, is_active=True).exists():
#             return JsonResponse({'error': 'Invalid or missing API key'}, status=403)
#         return self.get_response(request)
# myapp/middleware.py
from django.http import JsonResponse
from student.models import APIKey
import logging

logger = logging.getLogger(__name__)

class APIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/generate-api-key/':
            return self.get_response(request)

        api_key = request.headers.get('API-Key')
        logger.debug(f"Received API Key: {api_key}")
        if not api_key or not APIKey.objects.filter(key=api_key, is_active=True).exists():
            logger.debug("Invalid or missing API key")
            return JsonResponse({'error': 'Invalid or missing API key'}, status=403)
        return self.get_response(request)
