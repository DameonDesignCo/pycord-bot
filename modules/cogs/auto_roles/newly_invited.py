from datetime import datetime

import discord
from discord.ext import commands
from discord.utils import get


class NewlyInvited(commands.Cog, name="NewlyInvited Cog"):
    """Automatic guild role assignment"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        Assigns "Newly Invited" role to users when they first
        enter the server(guild) and send them a greeting in the #welcome channel
        :param member:
        :return:
        """
        role = get(member.guild.roles, name='Newly Invited')
        await member.add_roles(role)

        welcome = self.bot.get_channel(1078753426583863337)
        how_to_join = self.bot.get_channel(1022245292323651715)

        def welcome_embed():
            embed = discord.Embed(title=f"{member.mention} Welcome to the Gooneys Clan Server!",
                                  colour=0x00b0f4,
                                  timestamp=datetime.now())
            embed.set_author(name="from Gooneys Clan")
            embed.add_field(name="As you are new here...",
                            value=f"Head on over to the {how_to_join.mention} to continue your enrolment.")
            embed.set_image(
                url="https://www.looper.com/img/gallery/where-is-chunk-from-the-goonies-now/intro-1650944363.webp")
            embed.set_thumbnail(
                url="https://www.zbrushcentral.com/uploads/default/original"
                    "/4X/0/6/2/062e807505605854a4e7b311a8a472df1f7b2f66.jpeg")
            embed.set_footer(text="Hey you guyyyyyssss!",
                             icon_url="https://cdn-icons-png.flaticon.com/512/7297/7297895.png")
            return embed

        await welcome.send(embed=welcome_embed(), delete_after=7200)
        await member.send(embed=welcome_embed())


def setup(bot: commands.Bot):
    bot.add_cog(NewlyInvited(bot))
