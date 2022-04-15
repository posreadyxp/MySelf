from discord.ext import commands
from json import load, dump
import asyncio


class Prefix(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot
        with open("config.json", "r") as r:
            r = load(r)
            self.token = r["token"]
            self.write = r["write"]
            self.nitro_sniper = r["nitro_sniper"]

    @commands.group(name="prefix")
    async def prefix(self, ctx):
        if ctx.invoked_subcommand is None:
            async with ctx.typing():
                await asyncio.sleep(10)
            return await ctx.reply(
                """
```
~ - необязательно
! - обязательно

Доступные аргументы: 
prefix current
prefix change !prefix
```
                """
            )

    @prefix.command(name="current")
    async def prefix_current(self, ctx):
        with open("config.json", "r") as r:
            r = load(r)
            prefix = r["prefix"]
        return await ctx.reply(f"```Сейчас стоит префикс: {prefix}```")

    @prefix.command(name="change")
    async def prefix_change(self, ctx, prefix):
        if prefix:
            m = await ctx.reply("Ожидайте...")
            data = {
                "token": self.token,
                "write": self.write,
                "nitro_sniper": self.nitro_sniper,
                "prefix": prefix,
            }
            with open("config.json", "w") as r:
                dump(data, r, indent=4)
            await m.edit(content=f"Успешно поставлен префикс {prefix}")
        else:
            await ctx.reply("Эээ. Введи новый префикс!")


def setup(bot) -> None:
    bot.add_cog(Prefix(bot))
