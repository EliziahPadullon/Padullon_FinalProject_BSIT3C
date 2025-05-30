import jwt
from datetime import datetime, timedelta
from django.conf import settings

SECRET_KEY = getattr(settings, 'SECRET_KEY', 'your-default-secret-key')
ALGORITHM = 'HS256'

def generate_jwt(user):
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(days=1),  # token expires in 1 day
        'iat': datetime.utcnow(),                      # issued at
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
