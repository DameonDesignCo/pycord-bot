import discord
from discord import Option
from discord.ext.commands import Bot
from discord.ext.commands import slash_command
from discord.ext.commands import Cog


class Clear(Cog, name="Clear Messages"):
    """Clears messages from initiated channel"""

    @slash_command(
        name="clear",
        description="Delete Channel Messaged",
        guild_ids=[958031002029146123]
    )
    async def clear(self,
                    interaction: discord.Interaction,
                    clear_all: Option(bool,
                                      description="Clear All Messages"),
                    member: Option(discord.Member,
                                   description="Who's messages do you want to delete?",
                                   default="Everybody"),
                    amount: Option(int,
                                   description="How many messages to delete?",
                                   default=None)

                    ):
        self.amount = amount
        self.clear_all = clear_all
        self.member = member

        def _check(message):
            if self.clear_all:
                self.amount = self.history
                return True

            if self.amount is None:
                self.amount = self.history
            if self.deleted <= self.amount:
                if self.member == 'Everybody':
                    self.deleted += 1
                    return True
                if self.member != message.author:
                    return False
                else:
                    self.deleted += 1
                    return True
            else:
                print(f"END {self.deleted}")
                print(f"END {self.history}")
                return False

        async def _purge():
            num = 0
            for _ in await interaction.channel.purge(limit=100, check=_check):
                num += 1
            return num

        def blocks(n):
            remainder = n % 100
            if remainder == 0:
                _blocks = n / 100
                return _blocks
            else:
                _blocks = ((100 - remainder) + n) / 100
                return _blocks

        async def message_history():
            count = 0
            async for _ in interaction.channel.history(limit=None):
                count += 1
            return count

        async def bulk_divider():
            self.history = 0
            self.deleted = 0
            value = await message_history()
            self.history = value
            if value > 100:
                _value = int(blocks(value))
            else:
                _value = value
            for _ in range(_value):
                return await _purge()

        self.deleted = await bulk_divider()
        if self.deleted < 1:
            self.deleted = 0
        else:
            self.deleted = self.deleted - 1

        await interaction.response.send_message(f"{interaction.user.mention} deleted \n"
                                                f"{self.deleted} of {self.member}'s message(s)")

    def __init__(self, bot: Bot, amount=0, deleted=0, history=0, member='', clear_all=''):
        self.bot = bot
        self.amount = amount
        self.deleted = deleted
        self.history = history
        self.member = member
        self.clear_all = clear_all


def setup(bot: Bot):
    bot.add_cog(Clear(bot))
