import secrets
from django.http import JsonResponse
from functools import wraps
from .models import Student

def generate_bearer_token():
    return secrets.token_urlsafe(32)

def token_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token:
            try:
                token_type, token_key = token.split()
                if token_type == 'Bearer':
                    user = Student.objects.get(token=token_key)
                    request.user = user
                else:
                    return JsonResponse({'error': 'Invalid token type'}, status=401)
            except Student.DoesNotExist:
                return JsonResponse({'error': 'Invalid token'}, status=401)
            except ValueError:
                return JsonResponse({'error': 'Invalid token format'}, status=401)
        else:
            # Generate a new token if not provided
            new_token = generate_bearer_token()
            return JsonResponse({'token': new_token})
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view
