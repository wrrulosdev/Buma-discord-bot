from typing import Union

import discord
from loguru import logger
from discord.ext import commands

from ....constants import ChannelConstants

class ChannelUtils:
    @staticmethod
    async def get_channel_by_id(bot: commands.Bot, channel_id: int) -> Union[discord.channel.TextChannel, None]:
        """
        Get a channel by its ID.

        :param bot: The bot.
        :param channel_id: The ID of the channel.
        :return: The channel if found, None otherwise.
        """
        return bot.get_channel(channel_id)

    @staticmethod
    async def get_points_logs_channel(bot: commands.Bot) -> Union[discord.channel.TextChannel, None]:
        """
        Get the points logs channel.

        :return: The points logs channel if found, None otherwise.
        """
        try:
            channel_id: int = int(ChannelConstants.POINTS_LOGS_CHANNEL)

        except ValueError:
            logger.error('Invalid channel ID in the environment variables.')
            return None

        return await ChannelUtils.get_channel_by_id(bot=bot, channel_id=channel_id)
