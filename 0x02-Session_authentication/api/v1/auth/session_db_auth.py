#!/usr/bin/env python3
""" A progtram Module with storage support for
session authentication"""

from datetime import datetime, timedelta
from flask import request
from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """Session authenticatin class"""
    def create_session(self, user_id=None) -> str:
        """This function Creates session id"""
        sesh_id = super().create_session(user_id)

        if type(sesh_id) == str:
            kwargs = {
                'user_id': user_id,
                'session_id': sesh_id,
            }
            user_session = UserSession(**kwargs)
            user_session.save()
            return sesh_id

    def user_id_for_session_id(self, session_id=None):
        """ A function that returns user_id for
        a session_id"""
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        curr_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        exp_time = sessions[0].created_at + time_span
        if exp_time < curr_time:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        """ A function that Destroys an authenticated
        session"""
        sesh_id = self.session_cookie(request)

        try:
            sessions = UserSession.search({'session_id': sesh_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True
