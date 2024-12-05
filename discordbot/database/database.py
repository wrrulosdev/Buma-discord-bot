import sqlite3
import sys
import os

from typing import Optional
from contextlib import contextmanager

from loguru import logger


class Database:
    def __init__(self) -> None:
        if not os.path.exists('db'):
            os.makedirs('db')

        if not os.path.exists('db/buma.db'):
            open('db/buma.db', 'w').close()

        try:
            self.conn: sqlite3.Connection = sqlite3.connect('db/buma.db')

        except sqlite3.Error as e:
            logger.critical(f'Failed to connect to the database: {e}')
            sys.exit(1)

        self.create_table()

    @contextmanager
    def get_cursor(self):
        """Context manager for database cursor."""
        cursor: Optional[sqlite3.Cursor] = None

        try:
            cursor = self.conn.cursor()
            yield cursor

        except sqlite3.Error as e:
            logger.error(f'Database error: {e}')
            self.conn.rollback()
            raise

        finally:
            if cursor:
                cursor.close()

    def create_table(self) -> None:
        """Creates the users table if it doesn't exist."""
        try:
            with self.get_cursor() as cursor:
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    discord_id INTEGER PRIMARY KEY,
                    points INTEGER DEFAULT 0
                );
                ''')
                self.conn.commit()

        except sqlite3.Error as e:
            logger.critical(f'Failed to create table: {e}')
            sys.exit(1)

    def add_user(self, discord_id: int) -> bool:
        """
        Adds a new user to the database if not already exists.

        :param discord_id: The discord_id of the user.
        :return: True if successful, False otherwise.
        """
        try:
            with self.get_cursor() as cursor:
                cursor.execute('SELECT * FROM users WHERE discord_id = ?;', (discord_id,))

                if cursor.fetchone():
                    # logger.warning(f'User {discord_id} already exists.')
                    return False

                cursor.execute('INSERT INTO users (discord_id) VALUES (?);', (discord_id,))
                self.conn.commit()

            return True

        except sqlite3.Error as e:
            logger.error(f'Failed to add user: {e}')
            return False

    def remove_user(self, discord_id: int) -> bool:
        """
        Removes a user from the database.

        :param discord_id: The discord_id of the user.
        :return: True if successful, False otherwise.
        """
        try:
            with self.get_cursor() as cursor:
                cursor.execute('DELETE FROM users WHERE discord_id = ?;', (discord_id,))
                self.conn.commit()

            return True

        except sqlite3.Error as e:
            logger.error(f'Failed to remove user: {e}')
            return False

    def get_user(self, discord_id: int) -> Optional[dict]:
        """
        Fetches a user from the database by discord_id.

        :param discord_id: The discord_id of the user.
        :return: A dictionary containing the user's information. None if the user doesn't exist.
        """
        try:
            with self.get_cursor() as cursor:
                cursor.execute('SELECT * FROM users WHERE discord_id = ?;', (discord_id,))
                user: Optional[tuple] = cursor.fetchone()
                return {'discord_id': user[0], 'points': user[1]} if user else None

        except sqlite3.Error as e:
            logger.error(f'Failed to get user: {e}')
            return None

    def get_users(self) -> list:
        """
        Fetches all users from the database.

        :return: A list of users.
        """
        try:
            with self.get_cursor() as cursor:
                cursor.execute('SELECT * FROM users;')
                users: list[tuple] = cursor.fetchall()
                return [{"discord_id": user[0], "points": user[1]} for user in users]

        except sqlite3.Error as e:
            logger.error(f'Failed to get users: {e}')
            return []

    def add_points(self, discord_id: int, points: int) -> bool:
        """
        Adds points to a user's account.

        :param discord_id: The discord_id of the user.
        :param points: The amount of points to add.
        :return: True if successful, False otherwise.
        """
        try:
            if self.get_user(discord_id) is None:
                self.add_user(discord_id)

            with self.get_cursor() as cursor:
                cursor.execute('''
                UPDATE users SET points = points + ? WHERE discord_id = ?;
                ''', (points, discord_id))
                self.conn.commit()

            return True

        except sqlite3.Error as e:
            logger.error(f'Failed to add points: {e}')
            return False

    def remove_points(self, discord_id: int, points: int) -> bool:
        """
        Removes points from a user's account.

        :param discord_id: The discord_id of the user.
        :param points: The amount of points to remove.
        :return: True if successful, False otherwise.
        """
        try:
            user: Optional[dict] = self.get_user(discord_id)

            if user is None:
                logger.error(f'User {discord_id} not found. Cannot remove points.')
                return False

            with self.get_cursor() as cursor:
                cursor.execute('''
                UPDATE users SET points = points - ? WHERE discord_id = ?;
                ''', (points, discord_id))
                self.conn.commit()

            return True

        except sqlite3.Error as e:
            logger.error(f'Failed to remove points: {e}')
            return False

    def close(self) -> None:
        """Closes the database connection."""
        try:
            self.conn.close()
            logger.info('Database connection closed successfully.')

        except sqlite3.Error as e:
            logger.error(f'Failed to close database connection: {e}')
