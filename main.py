import os
import discord
from discord import ApplicationCommand
from discord.ext import commands

# keep alive for repl.it hosting
from webserver import keep_alive

GUILDS = [958031002029146123]

INTENTS = discord.Intents(
    auto_moderation_configuration=True,
    auto_moderation_execution=True,
    bans=True,
    dm_messages=True,
    dm_reactions=True,
    dm_typing=True,
    emojis=True,
    emojis_and_stickers=True,
    guild_messages=True,
    guild_reactions=True,
    guild_typing=True,
    guilds=True,
    integrations=True,
    invites=True,
    members=True,
    message_content=True,
    messages=True,
    presences=True,
    reactions=True,
    scheduled_events=True,
    typing=True,
    # value=True,
    voice_states=True,
    webhooks=True
)


class MyBot(commands.Bot):

    async def register_command(self, command: ApplicationCommand, force: bool = True,
                               guild_ids: list[int] | None = None) -> None:
        pass

    def __init__(self):
        super().__init__(
            command_prefix=">",
            intents=INTENTS,
            application_id=1075340756237176864
        )

        @self.event
        async def on_connect():
            if self.auto_sync_commands:
                await self.sync_commands()
            print(f"{self.user.name} bot: connected")

        @self.event
        async def on_ready():
            print(f"{self.user.name} bot is Ready")


def main():
    bot = MyBot()

    for folder in os.listdir("modules/cogs"):
        for file in os.listdir(f"modules/cogs/{folder}"):
            if file.endswith(".py"):
                if os.path.exists(os.path.join("modules", "cogs", folder, file)):
                    print(f"Cog: {file[:-3]}")
                    bot.load_extension(name=f"modules.cogs.{folder}.{file[:-3]}")

    keep_alive()
    bot.run(os.getenv("DISCORD_TOKEN"))


if __name__ == '__main__':
    main()
