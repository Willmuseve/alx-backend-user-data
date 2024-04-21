#!/usr/bin/env python3
"""Module function that expects one string argument name password and
returns a salted, hashed password, which is a byte string."""

import bcrypt


def hash_password(password: str) -> bytes:
    """Function hash_password"""
    return (bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Functin is_valid"""
    return (bcrypt.checkpw(password.encode('utf-8'), hashed_password))
