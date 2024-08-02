# decorators.py
import secrets
from functools import wraps
from django.http import JsonResponse, HttpResponseForbidden

# In-memory store for tokens (in a real app, use a secure database or cache)
TOKEN_STORE = {}

def generate_token():
    """Generate a random bearer token."""
    return secrets.token_urlsafe(32)

# def token_required(view_func):
#     @wraps(view_func)
#     def _wrapped_view(request, *args, **kwargs):
#         token = request.headers.get('Authorization')
#         if not token or not TOKEN_STORE.get(token):
#             return HttpResponseForbidden("Invalid or missing token.")
#         return view_func(request, *args, **kwargs)
#     return _wrapped_view

# def token_required(view_func):
#     @wraps(view_func)
#     def _wrapped_view(request, *args, **kwargs):
#         token = request.headers.get('Authorization')
#         if token:
#             token = token.split(" ")[-1]
#         print(f"Received token: {token}")  # Debug print
#         if not token or not TOKEN_STORE.get(token):
#             return HttpResponseForbidden("Invalid or missing token.")
#         return view_func(request, *args, **kwargs)
#     return _wrapped_view



def token_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        print(f"Authorization header: {auth_header}")  # Debug print
        if not auth_header:
            return HttpResponseForbidden("Missing token.")
        token = auth_header.split(" ")[1] if len(auth_header.split(" ")) > 1 else None
        print(f"Token extracted: {token}")  # Debug print
        if not token or not TOKEN_STORE.get(token):
            return HttpResponseForbidden("Invalid or missing token.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view




def generate_and_store_token():
    """Generate and store a new token."""
    token = generate_token()
    TOKEN_STORE[token] = True
    return token
