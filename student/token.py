
from functools import wraps
from django.http import JsonResponse

def token_required(func):
    @wraps(func)
    def wrap(request, *args, **kwargs):
        token = request.headers.get('Authorization')  
        expected_token = 'Bearer 6da5ffc1b3a291d2d3bfca7927cb6bfeaa4b1e6b' 

        if token != expected_token:
            return JsonResponse({'message': 'Please provide a valid token for authorization'}, status=401)

        return func(request, *args, **kwargs)

    return wrap