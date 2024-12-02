import discord
from loguru import logger

from ....constants import IDs


class AdminCheck:
    @staticmethod
    @logger.catch
    def is_admin(discord_id: int) -> bool:
        """
        Check if a user is an admin.
        :param discord_id: The ID of the user.
        :return: Whether the user is an admin.
        """
        return discord_id in IDs.ADMIN_IDS

    @staticmethod
    @logger.catch
    def is_from_dm(interaction: discord.Interaction) -> bool:
        """
        Check if the interaction is from a DM (Direct Message) channel.
        :param interaction: The interaction object.
        :return: Whether the interaction is from a DM channel.
        """
        return isinstance(interaction.channel, discord.DMChannel)
