from typing import Optional

from ....db import Database


class PointsUtils:
    @staticmethod
    def add_points_value_check(points: int) -> tuple[bool, Optional[str]]:
        """
        Check if the points value is valid.

        :param points: The points value.
        :return: True if valid, False otherwise.
        """
        if points < 0:
            return False, 'Invalid points value. Points must be greater than 0.'

        if points == 0:
            return False, 'Invalid points value. Points must be greater than 0.'

        return True, None

    @staticmethod
    def remove_points_value_check(discord_id: int, points: int) -> tuple[bool, Optional[str]]:
        """
        Check if the points value is valid.

        :param discord_id: The discord_id of the user.
        :param points: The points value.
        :return: True if valid, False otherwise.
        """
        if points < 0:
            return False, 'Invalid points value. Points must be greater than 0.'

        if points == 0:
            return False, 'Invalid points value. Points must be greater than 0.'

        user: Optional[dict] = Database().get_user(discord_id)

        if user is None:
            return False, 'User not found.'

        if user['points'] < points:
            return False, 'User does not have enough points.'

        return True, None
