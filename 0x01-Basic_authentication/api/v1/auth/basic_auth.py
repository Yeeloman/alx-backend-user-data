#!/usr/bin/env python3
"""imple for basic auth"""

from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import base64


class BasicAuth(Auth):
    """class that implements basic auth"""
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str | None:
        """as the name suggest lmao"""
        if not authorization_header \
            or not isinstance(authorization_header, str) \
                or not authorization_header.startswith('Basic '):
            return None
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str | None:
        """the decoded value of a Base64
        string base64_authorization_header"""
        if not base64_authorization_header:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """extract the credentials from usr:pswrd"""
        if not decoded_base64_authorization_header \
            or not isinstance(decoded_base64_authorization_header, str) \
                or ":" not in decoded_base64_authorization_header:
            return (None, None)
        return (
            decoded_base64_authorization_header[
                :decoded_base64_authorization_header.index(":")
                ],
            decoded_base64_authorization_header[
                decoded_base64_authorization_header.index(":") + 1:
                ],
            )

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """return a User instance
        based on email and password"""
        if not user_email \
            or not isinstance(user_email, str) \
                or not user_pwd or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for u in users:
                if u.is_valid_password(user_pwd):
                    return u
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """basic auth imple"""
        Auth_header = self.authorization_header(request)

        if Auth_header:
            token = self.extract_base64_authorization_header(Auth_header)
            if token:
                decoded = self.decode_base64_authorization_header(token)
                if decoded:
                    email, pwd = self.extract_user_credentials(decoded)
                    if email:
                        return self.user_object_from_credentials(email, pwd)
