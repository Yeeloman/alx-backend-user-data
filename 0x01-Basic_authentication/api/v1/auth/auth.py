#!/usr/bin/env python3
"""a class to manage
the API authentication."""


from flask import request
from typing import List, TypeVar


class Auth:
    """c lass that manages auth"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns True if the path is
        not in the list of strings excluded_paths"""
        if not path or not excluded_paths or len(excluded_paths) == 0:
            return True
        if path.endswith('/') and path in excluded_paths:
                return False
        if path + '/' in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str|None:
        """validate all requests to secure the API"""
        if not request:
            return None
        return request.headers.get("Authorization", None)


    def current_user(self, request=None) -> TypeVar('User')|None:
        """same"""
        if not request:
            return None
