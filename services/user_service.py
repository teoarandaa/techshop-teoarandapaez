"""
User service - Business logic for user operations.
Handles user registration, authentication, and validation.
"""

import bcrypt
import re
from typing import Optional, Dict
from models.user import User
from repositories.user_repository import UserRepository


class UserService:
    """
    Service for managing user operations.
    Handles registration, authentication, and password security.
    """
    
    # Validation patterns
    USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_]{4,20}$')
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    MIN_PASSWORD_LENGTH = 8
    
    @staticmethod
    def validate_username(username: str) -> Dict[str, any]:
        """
        Validate username format and availability.
        
        Rules:
        - 4-20 characters
        - Alphanumeric and underscore only
        - Must be unique
        
        Args:
            username: Username to validate
        
        Returns:
            dict: Result with 'valid' (bool) and 'message' (str)
        """
        if not username or len(username) < 4 or len(username) > 20:
            return {
                'valid': False,
                'message': "El nom d'usuari ha de tenir entre 4 i 20 caràcters."
            }
        
        if not UserService.USERNAME_PATTERN.match(username):
            return {
                'valid': False,
                'message': "El nom d'usuari només pot contenir lletres, números i guions baixos."
            }
        
        # Check uniqueness
        existing_user = UserRepository.find_by_username(username)
        if existing_user:
            return {
                'valid': False,
                'message': "Aquest nom d'usuari ja està en ús."
            }
        
        return {
            'valid': True,
            'message': ''
        }
    
    @staticmethod
    def validate_email(email: str) -> Dict[str, any]:
        """
        Validate email format and availability.
        
        Args:
            email: Email to validate
        
        Returns:
            dict: Result with 'valid' (bool) and 'message' (str)
        """
        if not email:
            return {
                'valid': False,
                'message': "L'email és obligatori."
            }
        
        if not UserService.EMAIL_PATTERN.match(email):
            return {
                'valid': False,
                'message': "Format d'email no vàlid."
            }
        
        # Check uniqueness
        existing_user = UserRepository.find_by_email(email)
        if existing_user:
            return {
                'valid': False,
                'message': "Aquest email ja està registrat."
            }
        
        return {
            'valid': True,
            'message': ''
        }
    
    @staticmethod
    def validate_password(password: str) -> Dict[str, any]:
        """
        Validate password strength.
        
        Rules:
        - Minimum 8 characters
        
        Args:
            password: Password to validate
        
        Returns:
            dict: Result with 'valid' (bool) and 'message' (str)
        """
        if not password or len(password) < UserService.MIN_PASSWORD_LENGTH:
            return {
                'valid': False,
                'message': f'La contrasenya ha de tenir almenys {UserService.MIN_PASSWORD_LENGTH} caràcters.'
            }
        
        return {
            'valid': True,
            'message': ''
        }
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password
        
        Returns:
            str: Hashed password
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            password: Plain text password
            password_hash: Hashed password
        
        Returns:
            bool: True if password matches, False otherwise
        """
        return bcrypt.checkpw(
            password.encode('utf-8'),
            password_hash.encode('utf-8')
        )
    
    @staticmethod
    def register_user(username: str, password: str, email: str) -> Dict[str, any]:
        """
        Register a new user with validation.
        
        Args:
            username: Username (4-20 characters)
            password: Password (minimum 8 characters)
            email: Email address
        
        Returns:
            dict: Result with 'success' (bool), 'message' (str), and 'user_id' (int)
        """
        # Validate username
        username_validation = UserService.validate_username(username)
        if not username_validation['valid']:
            return {
                'success': False,
                'message': username_validation['message']
            }
        
        # Validate email
        email_validation = UserService.validate_email(email)
        if not email_validation['valid']:
            return {
                'success': False,
                'message': email_validation['message']
            }
        
        # Validate password
        password_validation = UserService.validate_password(password)
        if not password_validation['valid']:
            return {
                'success': False,
                'message': password_validation['message']
            }
        
        try:
            # Hash password
            password_hash = UserService.hash_password(password)
            
            # Create user
            user = User(
                username=username,
                password_hash=password_hash,
                email=email
            )
            
            user_id = UserRepository.create(user)
            
            return {
                'success': True,
                'message': 'Usuari registrat correctament.',
                'user_id': user_id
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Error en registrar usuari: {str(e)}'
            }
    
    @staticmethod
    def authenticate(username: str, password: str) -> Optional[User]:
        """
        Authenticate a user by username and password.
        
        Args:
            username: Username
            password: Plain text password
        
        Returns:
            User: User instance if authentication successful, None otherwise
        """
        user = UserRepository.find_by_username(username)
        
        if not user:
            return None
        
        if UserService.verify_password(password, user.password_hash):
            return user
        
        return None

