#!/usr/bin/env python3
"""impl of expiration date"""

import datetime as dt
import os
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """an expiration date to a Session ID"""
    def __init__(self):
        """initiate an instance of the class"""
        try:
            tmp = int(os.getenv('SESSION_DURATION'))
        except Exception as _:
            tmp = 0
        self.session_duration = tmp

    def create_session(self, user_id=None):
        """creates a session"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dict = {
            "user_id": user_id,
            "created_at": dt.datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """overrides the super class"""
        if session_id is None:
            return None
        user_details = self.user_id_by_session_id.get(session_id)
        if user_details is None:
            return None
        if "created_at" not in user_details.keys():
            return None
        if self.session_duration <= 0:
            return user_details.get("user_id")
        created_at = user_details.get("created_at")
        allowed_win = created_at + dt.timedelta(seconds=self.session_duration)
        if allowed_win < dt.datetime.now():
            return None
        return user_details.get("user_id")
