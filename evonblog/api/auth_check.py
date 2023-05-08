import jwt
from jwt.exceptions import ExpiredSignatureError
from rest_framework.response import Response
from rest_framework import status

jwt_secret_token = "evonblog_tokens"
def auth_check(token):
    print(token)
    decoded_token = {}
    try:
        decoded_token = jwt.decode(token, jwt_secret_token, algorithms=['HS256'])
        return decoded_token
    except ExpiredSignatureError:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response({'error': 'Invalid Auth Token'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # return decoded_token