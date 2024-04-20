#!/usr/bin/env python3
"""Module for Session authentication with expiration date"""

import os
from datetime import datetime, timedelta
from flask import request
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """A Class that inherits from SessionAuth and adds
    expiration date to a session ID.
    """
    def __init__(self) -> None:
        """ The init function that Initialises
        the class"""
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """A function that creates a session id"""
        sesh_id = super().create_session(user_id)

        if type(sesh_id) != str:
            return None
        self.user_id_by_session_id[sesh_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        return sesh_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """ A function that Returns user_id for a session_id"""
        if session_id in self.user_id_by_session_id:
            sesh_dict = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return sesh_dict['user_id']
            if 'created_at' not in sesh_dict:
                return None
            curr_time = datetime.now()
            time_span = timedelta(seconds=self.session_duration)
            exp_time = sesh_dict['created_at'] + time_span

            if exp_time < curr_time:
                return None
            return sesh_dict['user_id']
