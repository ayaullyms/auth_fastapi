import time
import jwt
from decouple import config

JWT_SECRET = config('JWT_SECRET')
JWT_ALGORITHM = config('JWT_ALGORITHM')

def signJWT(user_id: str):
    payload = {
        'user_id': user_id,
        'expires': time.time() + 600 
    }
    token = jwt.encode(payload, key=JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    return { "access_token": token }

def decodeJWT(token: str):
    decoded_token = jwt.decode(token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
    return decoded_token if decoded_token["expires"] >= time.time() else None 

    # if decoded_token >= time.time():
    #     return decoded_token
    # else:
    #     return None