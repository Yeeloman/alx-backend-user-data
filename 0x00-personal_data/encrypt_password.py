#!/usr/bin/env python3
"""Encrypting passwords
Check valid password"""

import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password,
    which is a byte string."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """checks if a pswrd is valid"""
    return bcrypt.checkpw(password.encode(), hashed_password)
