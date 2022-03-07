import asyncio
import discord
from discord.ext import commands


class Statuses(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot
        self.statuses = {
            "online": discord.Status.online,
            "offline": discord.Status.offline,
            "dnd": discord.Status.dnd,
            "idle": discord.Status.idle
        }

    @commands.group(name="status")
    async def status(self, ctx):
        if ctx.invoked_subcommand is None:
            async with ctx.typing():
                await asyncio.sleep(10)
            return await ctx.send(
                """
```
~ - необязательно
! - обязательно

Доступные аргументы: 
online ~текст статуса
idle ~текст статуса
dnd ~текст статуса
offline
stream !текст статуса
```
                """
            )

    @status.command(name="online")
    async def status_online(self, ctx, arg: str = None):
        if not arg:
            await self.bot.change_presence(status=self.statuses["online"])
        else:
            await self.bot.change_presence(
                activity=discord.Game(name=arg), status=self.statuses["online"]
            )

    @status.command(name="idle")
    async def status_idle(self, ctx, arg: str = None):
        if not arg:
            await self.bot.change_presence(status=self.statuses["idle"])
        else:
            await self.bot.change_presence(
                activity=discord.Game(name=arg), status=self.statuses["idle"]
            )

    @status.command(name="dnd")
    async def status_dnd(self, ctx, arg: str = None):
        if not arg:
            await self.bot.change_presence(status=self.statuses["dnd"])
        else:
            await self.bot.change_presence(
                activity=discord.Game(name=arg), status=self.statuses["dnd"]
            )

    @status.command(name="offline")
    async def status_offline(self, ctx, arg: str = None):
        if not arg:
            await self.bot.change_presence(status=self.statuses["offline"])
        else:
            await self.bot.change_presence(
                activity=discord.Game(name=arg), status=self.statuses["offline"]
            )

    @status.command(name="stream")
    async def status_stream(self, ctx, arg: str = None):
        if not arg:
            await ctx.send("Введи текст для статуса!")
        else:
            await self.bot.change_presence(
                activity=discord.Streaming(name=arg, url="https://twitch.tv/twitch")
            )

def setup(bot) -> None:
    bot.add_cog(Statuses(bot))
