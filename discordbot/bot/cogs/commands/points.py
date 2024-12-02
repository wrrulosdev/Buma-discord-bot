import asyncio
from typing import Optional

import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import has_permissions
from loguru import logger

from discordbot.bot.utils.admin.utils import AdminCheck

from ....db import Database
from ...utils import ChannelUtils, PointsUtils, EmbedUtilities


class Points(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    points: app_commands.Group = app_commands.Group(name='points', description='Points system commands')

    @points.command(name='add', description='Add points to a user')
    @logger.catch
    async def add_points(self, interaction: discord.Interaction, user: discord.User, points: int, reason: str) -> None:
        """
        Add points to a user.

        :param interaction: The interaction object.
        :param user: The user to add points to.
        :param points: The amount of points to add.
        rtype: The reason for adding points.
        """
        if not AdminCheck.is_admin(interaction.user.id):
            await interaction.response.send_message('You do not have permission to use this command.', ephemeral=True)
            return

        if user.bot:
            await interaction.response.send_message('You cannot add points to a bot.', ephemeral=True)
            return

        check: tuple[bool, Optional[str]] = PointsUtils.add_points_value_check(points)

        if not check[0]:
            await interaction.response.send_message(check[1], ephemeral=True)
            return

        output: bool = Database().add_points(user.id, points)

        if not output:
            await interaction.response.send_message('Failed to add points. Read the logs for more information.', ephemeral=True)
            return

        await interaction.response.send_message(f'Added {points} points to {user.name}', ephemeral=True)
        points_logs_channel: Optional[discord.TextChannel] = await ChannelUtils.get_points_logs_channel(self.bot)

        if points_logs_channel is None:
            logger.error('Points logs channel not found.')
            return

        embed: discord.Embed = EmbedUtilities.create_embed(
            title=f'{user.name} Obtained {points} Points!',
            description=f'Reason: {reason}',
            color=discord.Color.red(),
            footer='Furnihome',
            image='https://imgur.com/QVmQXpn.png'
        )
        await points_logs_channel.send(embed=embed)
        message: discord.Message = await points_logs_channel.send(content=user.mention)
        await asyncio.sleep(1)
        await message.delete()

    @points.command(name='remove', description='Remove points from a user')
    @has_permissions(administrator=True)
    @logger.catch
    async def remove_points(self, interaction: discord.Interaction, user: discord.User, points: int) -> None:
        """
        Remove points from a user.

        :param interaction: The interaction object.
        :param user: The user to remove points from.
        :param points: The amount of points to remove.
        """
        if not AdminCheck.is_admin(interaction.user.id):
            await interaction.response.send_message('You do not have permission to use this command.', ephemeral=True)
            return

        if user.bot:
            await interaction.response.send_message('You cannot remove points from a bot.', ephemeral=True)
            return

        check: tuple[bool, Optional[str]] = PointsUtils.remove_points_value_check(user.id, points)

        if not check[0]:
            await interaction.response.send_message(check[1], ephemeral=True)
            return

        output: bool = Database().remove_points(user.id, points)

        if not output:
            await interaction.response.send_message('Failed to remove points. Read the logs for more information.', ephemeral=True)
            return

        await interaction.response.send_message(f'Removed {points} points from {user.name}', ephemeral=True)

    @points.command(name='view', description='Get the points of a user')
    @has_permissions(administrator=True)
    @logger.catch
    async def get_points(self, interaction: discord.Interaction, user: discord.User) -> None:
        """
        Get the points of a user.

        :param interaction: The interaction object.
        :param user: The user to get the points of.
        """
        if not AdminCheck.is_admin(interaction.user.id):
            await interaction.response.send_message('You do not have permission to use this command.', ephemeral=True)
            return

        user_data: Optional[dict] = Database().get_user(user.id)

        if user_data is None:
            # Return 0 points if the user doesn't exist in the database
            await interaction.response.send_message(f'{user.name} has 0 points', ephemeral=True)
            return None

        embed: discord.Embed = EmbedUtilities.create_embed(
            title=f'Points of **{user.name}**',
            description=f'This user has {user_data["points"]} points',
            color=discord.Color.red(),
            footer='Furnihome'
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Points(bot))
