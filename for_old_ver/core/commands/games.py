from enum import Enum
import json
import discord
from discord.ext import commands
from aiohttp import request

with open("config.json", "r") as r:
    config = json.load(r)


class Activity(Enum):
    betrayal = 0
    fishington = 1
    youtube = 2
    doodle = 3
    word_snacks = 4
    sketch = 5


class GamesActivity:
    def __init__(self) -> None:
        """
        Initialization
        """
        pass

    async def new_activity(
        self, channel, activity: Activity, activity_id: int = None
    ) -> str:
        """
        Creates an invite link with entered activity

        Params
        -------
        activity
            The activity to create invite link
        activity_id
            The ID of the activity to create link
            (worked if ``activity`` is ``Activity.custom``)

        Returns
        --------
            The invite link to launch specific activity

        Return type
        ------------
            :class:`str`
        """

        # async def _create_inv_link(activity_id: int):
        #     return await self.create_invite(
        #         target_type=discord.InviteTarget.embedded_application,
        #         target_application_id=activity_id
        #     )

        async def _create_inv_link(activity_id: int):
            data = {
                "max_age": 0,
                "max_uses": 0,
                "target_application_id": activity_id,
                "target_type": 2,
                "temporary": False,
                "validate": None,
            }
            async with request(
                "POST",
                f"https://discord.com/api/v9/channels/{channel.id}/invites",
                data=json.dumps(data),
                headers={
                    "Authorization": config["token"],
                    "Content-Type": "application/json",
                },
            ) as r:
                link = json.loads(await r.text())
            return f"https://discord.com/invite/{link['code']}"

        if activity == Activity.betrayal:
            return await _create_inv_link(773336526917861400)
        elif activity == Activity.fishington:
            return await _create_inv_link(814288819477020702)
        elif activity == Activity.youtube:
            return await _create_inv_link(880218394199220334)
        elif activity == Activity.doodle:
            return await _create_inv_link(878067389634314250)
        elif activity == Activity.word_snacks:
            return await _create_inv_link(879863976006127627)
        elif activity == Activity.sketch:
            return await _create_inv_link(902271654783242291)

    discord.VoiceChannel.create_activity_invite = new_activity


class Games(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot
        self.activity_game = GamesActivity()

    @commands.group(name="games")
    async def games(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(
                """
```
Доступные аргументы:

betrayal
fishington
youtube
doodle
word_snacks
sketch
```
            """
            )

    @games.command(name="betrayal")
    async def games_betrayal(self, ctx, channel: discord.VoiceChannel):
        if channel:
            invite = await self.activity_game.new_activity(channel, Activity.betrayal)
            await ctx.send(invite)
        else:
            await ctx.reply("Такого голосового канала нет!")

    @games.command(name="fishington")
    async def games_fishington(self, ctx, channel: discord.VoiceChannel):
        if channel:
            invite = await self.activity_game.new_activity(channel, Activity.fishington)
            await ctx.send(invite)
        else:
            await ctx.reply("Такого голосового канала нет!")

    @games.command(name="youtube")
    async def games_youbube(self, ctx, channel: discord.VoiceChannel):
        if channel:
            invite = await self.activity_game.new_activity(channel, Activity.youtube)
            await ctx.send(invite)
        else:
            await ctx.reply("Такого голосового канала нет!")

    @games.command(name="doodle")
    async def games_doodle(self, ctx, channel: discord.VoiceChannel):
        if channel:
            invite = await self.activity_game.new_activity(channel, Activity.doodle)
            await ctx.send(invite)
        else:
            await ctx.reply("Такого голосового канала нет!")

    @games.command(name="sketch")
    async def games_sketch(self, ctx, channel: discord.VoiceChannel):
        if channel:
            invite = await self.activity_game.new_activity(channel, Activity.sketch)
            await ctx.send(invite)
        else:
            await ctx.reply("Такого голосового канала нет!")


def setup(bot) -> None:
    bot.add_cog(Games(bot))
