"""
User repository - Data access layer for User entity.
"""

from typing import Optional, List
from models.user import User
from database import db


class UserRepository:
    """
    Repository for User data access operations.
    Separates database operations from business logic.
    """
    
    @staticmethod
    def create(user: User) -> int:
        """
        Insert a new user into the database.
        
        Args:
            user: User instance to insert
        
        Returns:
            int: ID of the newly created user
        
        Raises:
            Exception: If username or email already exists
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO "user" (username, password_hash, email, created_at, edat, segment, ciutat, provincia, pais)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (user.username, user.password_hash, user.email, user.created_at,
                 user.edat, user.segment, user.ciutat, user.provincia, user.pais)
            )
            return cursor.fetchone()[0]
    
    @staticmethod
    def find_by_id(user_id: int) -> Optional[User]:
        """
        Find a user by their ID.
        
        Args:
            user_id: User ID to search for
        
        Returns:
            User instance if found, None otherwise
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM "user" WHERE id = %s',
                (user_id,)
            )
            row = cursor.fetchone()

            if row:
                return User(
                    id=row[0], username=row[1], password_hash=row[2],
                    email=row[3], created_at=row[4],
                    edat=row[5], segment=row[6] or '',
                    ciutat=row[7] or '', provincia=row[8] or '', pais=row[9] or ''
                )
            return None

    @staticmethod
    def find_by_username(username: str) -> Optional[User]:
        """
        Find a user by their username.
        
        Args:
            username: Username to search for
        
        Returns:
            User instance if found, None otherwise
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM "user" WHERE username = %s',
                (username,)
            )
            row = cursor.fetchone()

            if row:
                return User(
                    id=row[0], username=row[1], password_hash=row[2],
                    email=row[3], created_at=row[4],
                    edat=row[5], segment=row[6] or '',
                    ciutat=row[7] or '', provincia=row[8] or '', pais=row[9] or ''
                )
            return None

    @staticmethod
    def find_by_email(email: str) -> Optional[User]:
        """
        Find a user by their email.
        
        Args:
            email: Email to search for
        
        Returns:
            User instance if found, None otherwise
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM "user" WHERE email = %s',
                (email,)
            )
            row = cursor.fetchone()

            if row:
                return User(
                    id=row[0], username=row[1], password_hash=row[2],
                    email=row[3], created_at=row[4],
                    edat=row[5], segment=row[6] or '',
                    ciutat=row[7] or '', provincia=row[8] or '', pais=row[9] or ''
                )
            return None

    @staticmethod
    def get_all() -> List[User]:
        """
        Retrieve all users from the database.
        
        Returns:
            List of User instances
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM "user"')
            rows = cursor.fetchall()

            return [
                User(
                    id=row[0], username=row[1], password_hash=row[2],
                    email=row[3], created_at=row[4],
                    edat=row[5], segment=row[6] or '',
                    ciutat=row[7] or '', provincia=row[8] or '', pais=row[9] or ''
                )
                for row in rows
            ]

