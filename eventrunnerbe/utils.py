from django.contrib.auth import authenticate
import json
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.backends import TokenBackend
from typing import Any, Optional, Union
#from .settings import api_settings
from rest_framework_simplejwt.tokens import Token

import jwt
import requests

def jwt_get_username_from_payload_handler(payload):
    username = payload.get('sub').replace('|', '.')
    print(username)
    authenticate(remote_user=username)
    return username


def jwt_decode_token(token):
    header = jwt.get_unverified_header(token)
    jwks = requests.get('https://{}/.well-known/jwks.json'.format('dev-x8hbr3jrn2mxvw4x.us.auth0.com')).json()
    public_key = None
    for jwk in jwks['keys']:
        if jwk['kid'] == header['kid']:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception('Public key not found.')

    issuer = 'https://{}/'.format('dev-x8hbr3jrn2mxvw4x.us.auth0.com')
    return jwt.decode(token, public_key, audience='https://eventrunner.com/api/', issuer=issuer, algorithms=['RS256'])

class customJWTAuth(JWTAuthentication):
    def authenticate(self, request):

        user = super().authenticate(request)
        if user is not None:
            request.user = user[0]
            return user
        return None

    def enforce_csrf(self, request):
        return  # No CSRF validation for JWT authentication
    
#class customTokenBackend(TokenBackend):
    #def _prepare_key(self, key: Optional[str]) -> Any:
        # Support for PyJWT 1.7.1 or empty signing key
        #if key is None or not getattr(jwt.PyJWS, "get_algorithm_by_name", None):
        #    return key
        #jws_alg = jwt.PyJWS().get_algorithm_by_name(self.algorithm)
        #print(self.algorithm)
        #return super()._prepare_key(Optional[str])
    
#    #@cached_property
#    def prepared_signing_key(self) -> Any:
#        print(self.algorithm)
#        return self._prepare_key(self.signing_key)
    
#class CustomJWTAuthentication(JWTAuthentication):
    #def _prepare_key(self, key: Optional[str]) -> Any:
        # Support for PyJWT 1.7.1 or empty signing key
        #if key is None or not getattr(jwt.PyJWS, "get_algorithm_by_name", None):
        #    return key
        #jws_alg = jwt.PyJWS().get_algorithm_by_name(self.algorithm)
        #print(self.algorithm)
        #return super()._prepare_key(Optional[str])
    
#    def get_validated_token(self, raw_token: bytes) -> Token:
#        """
#        Validates an encoded JSON web token and returns a validated token
#        wrapper object.
#        """
#        messages = []
#        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
#            print(AuthToken)

#        return super().get_validated_token(raw_token)