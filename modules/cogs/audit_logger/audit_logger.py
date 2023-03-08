import logging
from datetime import datetime

import discord
from discord.ext import commands


class AuditLogger(commands.Cog, name="AuditLogger Cog"):
    """Automatic guild role assignment"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        log_channel = self.bot.get_channel(1073305123670982778)
        embed = discord.Embed(title=f"{message.author.name}'s message was DELETED",
                              timestamp=datetime.now(),
                              colour=discord.Color.red())
        embed.add_field(name='Content:', value=message.content, inline=False)
        embed.add_field(name='Author:', value=message.author.mention, inline=True)
        embed.add_field(name='Channel:', value=message.channel.mention, inline=True)
        embed.set_author(name=message.author, icon_url=message.author.display_avatar)
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        log_channel = self.bot.get_channel(1073305123670982778)
        embed = discord.Embed(title=f"{before.author.name}'s message was EDITED",
                              description=f"Before: {before.content}\n"
                                          f"After: {after.content}\n"
                                          f"Author: {before.author.mention}\n"
                                          f"Location: {before.channel.mention}\n",
                              timestamp=datetime.now(),
                              colour=discord.Color.blue())
        embed.set_author(name=before.author.nick, icon_url=before.author.display_avatar)
        embed.set_thumbnail(url=before.author.display_avatar)
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        log_channel = self.bot.get_channel(1073305123670982778)

        def roles():
            """
            User Role Updates
            :return:
            """

            # Role removed
            if len(before.roles) > len(after.roles):
                role = next(role for role in before.roles if role not in after.roles)
                _embed = discord.Embed(title=f"{before.nick} updated",
                                       description=f"{role.name} role was REMOVED",
                                       timestamp=datetime.now(),
                                       colour=discord.Color.red()
                                       )
                _embed.set_author(name=before.name, icon_url=before.display_avatar)
                _embed.set_thumbnail(url=before.display_avatar)
                return _embed
                # Role added
            elif len(after.roles) > len(before.roles):
                role = next(role for role in after.roles if role not in before.roles)
                _embed = discord.Embed(title=f"{after.nick} updated",
                                       description=f"{role.name} role was ADDED",
                                       timestamp=datetime.now(),
                                       colour=discord.Color.blue()
                                       )
                _embed.set_author(name=before.name, icon_url=before.display_avatar)
                _embed.set_thumbnail(url=before.display_avatar)
                return _embed

        def nickname():
            # Nickname updated
            if before.nick != after.nick:
                _embed = discord.Embed(title=f"{before.nick}'s nickname CHANGED",
                                       description=f"Before: {before.nick}\n"
                                                   f"After: {after.nick}",
                                       timestamp=datetime.now(),
                                       colour=discord.Color.red()
                                       )
                _embed.set_author(name=before.name, icon_url=before.display_avatar)
                _embed.set_thumbnail(url=before.display_avatar)
                return _embed

        for fn in [roles, nickname]:
            try:
                x = fn()
                if x is not None:
                    embed = fn()
                    await log_channel.send(embed=embed)
            except Exception as e:
                logging.exception(e)
            # return

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        log_channel = self.bot.get_channel(1073305123670982778)

        def avatar():
            if before.avatar != after.avatar:
                _embed = discord.Embed(title=f"{after.avatar} updated",
                                       description=f"{after.name}'s Avatar was Changed",
                                       timestamp=datetime.now(),
                                       colour=discord.Color.blue()
                                       )
                return _embed

        def username():
            if before.User.name != after.User.name:
                _embed = discord.Embed(title=f"{after.avatar} updated",
                                       description=f"{after.name}'s Avatar was Changed",
                                       timestamp=datetime.now(),
                                       colour=discord.Color.blue()
                                       )
                return _embed
        for fn in [avatar, username]:
            try:
                embed = fn()
                embed.set_author(name=after.name.mention, icon_url=after.display_avatar)
                embed.set_thumbnail(url=after.author.display_avatar)
                await log_channel.send(embed=embed)
            except:
                return


def setup(bot: commands.Bot):
    bot.add_cog(AuditLogger(bot))
