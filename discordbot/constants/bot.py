import os
from typing import Optional, Any

from dotenv import load_dotenv

load_dotenv()


class BotConstants:
    COGS_PATH: str = 'discordbot/bot/cogs'  # Change this if you rename the folder
    COG_PATH: str = 'discordbot.bot.cogs'  # Change this if you rename the folder
    TOKEN: Optional[str] = os.getenv('DISCORD_TOKEN')


class ChannelConstants:
    POINTS_LOGS_CHANNEL: Any = os.getenv('POINTS_LOGS_CHANNEL')


class IDs:
    ADMIN_IDS: list[int] = [1257797619078660096, 772531685438783539]
