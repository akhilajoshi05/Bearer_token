import jwt
from datetime import datetime, timedelta
from functools import wraps
from django.http import JsonResponse

SECRET_KEY = 'your_secret_key'

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(minutes=30),  # Token expires in 30 minutes
        'iat': datetime.utcnow()  # Issued at time
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    @wraps(f)
    def decorated(request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return JsonResponse({'message': 'Token is missing!'}, status=403)

        try:
            token = token.split()[1]
            user_id = decode_token(token)
            if not user_id:
                return JsonResponse({'message': 'Token is invalid!'}, status=403)
        except IndexError:
            return JsonResponse({'message': 'Token format is invalid!'}, status=403)

        request.user_id = user_id
        return f(request, *args, **kwargs)

    return decorated
