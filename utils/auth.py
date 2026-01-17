import hashlib
import secrets
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class AuthManager:
    def __init__(self):
        self.users = {}
        self.sessions = {}
        self._init_default_users()
    
    def _init_default_users(self):
        self.users = {
            "user1": {
                "password_hash": self._hash_password("password123"),
                "profile": "CDI",
                "role": "employee"
            },
            "admin": {
                "password_hash": self._hash_password("admin123"),
                "profile": "Cadre",
                "role": "admin"
            }
        }
    
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username: str, password: str) -> Optional[Dict]:
        if username not in self.users:
            return None
        
        user = self.users[username]
        if user["password_hash"] != self._hash_password(password):
            return None
        
        session_token = secrets.token_urlsafe(32)
        self.sessions[session_token] = {
            "username": username,
            "profile": user["profile"],
            "role": user["role"]
        }
        
        return {
            "token": session_token,
            "username": username,
            "profile": user["profile"],
            "role": user["role"]
        }
    
    def verify_token(self, token: str) -> Optional[Dict]:
        return self.sessions.get(token)
    
    def logout(self, token: str) -> bool:
        if token in self.sessions:
            del self.sessions[token]
            return True
        return False
    
    def get_user_profile(self, token: str) -> Optional[str]:
        session = self.verify_token(token)
        return session["profile"] if session else None
