import json
import logging

import jwt
import requests
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication

logger = logging.getLogger(__name__)

AUTH0_DOMAIN = 'dev-x8hbr3jrn2mxvw4x.us.auth0.com'
AUTH0_AUDIENCE = 'https://eventrunner.com/api/'


def jwt_get_username_from_payload_handler(payload):
    sub = payload.get('sub')
    if not sub:
        logger.warning("JWT payload missing sub claim")
        raise ValueError("Invalid token payload: missing sub.")

    username = sub.replace('|', '.')
    logger.debug("Authenticating remote user from JWT payload")

    user = authenticate(remote_user=username)
    if user is None:
        logger.warning("Remote user authentication failed", extra={"username": username})

    return username


def jwt_decode_token(token):
    try:
        header = jwt.get_unverified_header(token)
    except jwt.PyJWTError:
        logger.warning("Invalid JWT token header")
        raise ValueError("Invalid token.") from None

    try:
        jwks_response = requests.get(
            f'https://{AUTH0_DOMAIN}/.well-known/jwks.json',
            timeout=10,
        )
        jwks_response.raise_for_status()
        jwks = jwks_response.json()
    except requests.RequestException:
        logger.exception("Failed to fetch Auth0 JWKS")
        raise ValueError("Unable to validate token.") from None

    public_key = None
    for jwk in jwks.get('keys', []):
        if jwk.get('kid') == header.get('kid'):
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
            break

    if public_key is None:
        logger.error("Auth0 public key not found", extra={"kid": header.get('kid')})
        raise ValueError('Public key not found.')

    issuer = f'https://{AUTH0_DOMAIN}/'
    try:
        return jwt.decode(
            token,
            public_key,
            audience=AUTH0_AUDIENCE,
            issuer=issuer,
            algorithms=['RS256'],
        )
    except jwt.PyJWTError:
        logger.warning("JWT decode failed")
        raise ValueError("Invalid token.") from None


class customJWTAuth(JWTAuthentication):
    def authenticate(self, request):
        user = super().authenticate(request)
        if user is not None:
            request.user = user[0]
            return user
        return None

    def enforce_csrf(self, request):
        return
