#!/usr/bin/env python3
"""UserSession that inherits from base"""

from models.base import Base


class UserSession(Base):
    """imple of UserSession to keep
    user in the db"""
    def __init__(self, *args: list, **kwargs: dict):
        """initiate an instance"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
