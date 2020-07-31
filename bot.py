"""
Created by vcokltfre - 2020-07-15
"""

import discord
from discord.ext import commands
from discord.ext.commands import has_any_role
import time

import logging
from salbotlp_secrets.config import TOKEN
import helpers.config as config

logger = logging.getLogger("salbot_lp")


class Bot(commands.Bot):
    """A subclassed version of commands.Bot"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    async def on_message_edit(before: discord.Message, after: discord.Message):
        await self.process_commands(after)

    def add_cog(self, cog: commands.Cog) -> None:
        """Adds a cog to the bot and logs it."""
        super().add_cog(cog)
        logger.info(f"Cog loaded: {cog.qualified_name}")

    def load_extensions(self, cogs: list):
        """Loads a list of cogs"""
        for cog in cogs:
            try:
                super().load_extension(cog)
                logger.info(f"Loaded cog {cog} successfully.")
            except Exception as e:
                logger.error(f"Failed to load cog {cog}.")
                print(e)

    async def on_error(self, event: str, *args, **kwargs) -> None:
        """Log errors raised in event listeners rather than printing them to stderr."""

        logger.exception(f"Unhandled exception in {event}.", exc_info=True)


if __name__ == "__main__":
    bot = Bot(
        command_prefix=commands.when_mentioned_or("%"),
        max_messages=10000,
        #allowed_mentions=discord.AllowedMentions(everyone=False, users=True, roles=False), #if this is your server you want this enabled, for sblp those perms are off anyway
        help_command=commands.MinimalHelpCommand()
        )

    @bot.command(name="restart")
    @has_any_role("Administrator", "Moderator")
    async def restart(ctx: commands.Context):
        cfg = config.ConfigUtil("rslock", {"lock": 0})
        cfg.write({"lock": round(time.time() + 30), "channel": ctx.channel.id})
        await ctx.channel.send("Restarting SalC1 Bot...")
        logger.info("Shutting down salbotlp")
        await bot.logout()

    cogs = ["cogs.translate", "cogs.dadbot", "cogs.profile", "cogs.errorhandler", "cogs.muffin", "cogs.convert", "cogs.general", "cogs.startup", "cogs.rplace", "cogs.tts"]

    bot.load_extensions(cogs)
    bot.run(TOKEN)
