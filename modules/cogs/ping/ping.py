import discord
from discord.ext import commands


class Ping(commands.Cog, name="Ping Cog"):
    """Receives ping commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="ping",
        description="Ping Pong Slash Command",
        guild_ids=[958031002029146123]
    )
    async def ping(self, interaction: discord.Interaction):
        """Checks for a response from the bot"""
        await interaction.response.send_message("Pong")


def setup(bot: commands.Bot):
    bot.add_cog(Ping(bot))
