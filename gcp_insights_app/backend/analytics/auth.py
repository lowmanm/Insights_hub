"""
Custom authentication classes for integrating Saviynt with Django REST
Framework.

Saviynt uses the concept of *Scramble Id* for user identity and
entitlement management.  Because the details of your Saviynt
deployment are private to your organisation, this module provides
stubbed classes that demonstrate how you might hook into the Django
authentication system.  Replace the placeholders with calls to
Saviynt’s APIs or middleware as appropriate.
"""

from typing import Optional, Tuple

from django.contrib.auth.models import AnonymousUser, User
from rest_framework import authentication, exceptions


class SaviyntAuthentication(authentication.BaseAuthentication):
    """Authenticate requests using Saviynt Scramble Id.

    In your real implementation this class would extract an
    authentication token or Scramble Id from the incoming request
    headers, validate it against Saviynt’s API, and return a Django
    `User` object representing the authenticated principal.
    """

    def authenticate(self, request) -> Optional[Tuple[User, None]]:
        scramble_id = request.headers.get('X-Scramble-Id')
        if not scramble_id:
            # No authentication header means unauthenticated
            return None

        # TODO: Call Saviynt API to validate scramble_id and retrieve user info
        # For now we simply create or get a Django user using the scramble id as
        # the username.  Replace this logic with actual validation and user lookup.
        try:
            user, _ = User.objects.get_or_create(username=scramble_id)
            return (user, None)
        except Exception as exc:
            raise exceptions.AuthenticationFailed(f'Failed to authenticate: {exc}')
