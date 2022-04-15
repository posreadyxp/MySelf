from discord.ext import commands
from aiohttp import request
from discord import ChannelType, Role, StageChannel, TextChannel, VoiceChannel


class Cloner(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.command()
    async def ладно(self, ctx):
        if not ctx.guild:
            return
#         m = await ctx.send(
#             """
# :hourglass: - создание сервера
# :x: - удалены все каналы с сервера и роли
# :x: - созданы каналы
# :x: - созданы роли
# :х: - полностью создан сервер
#         """
#         )
        if ctx.guild.icon:
            async with request("GET", str(ctx.guild.icon)) as r:
                new_guild = await self.bot.create_guild(
                    name=ctx.guild.name, icon=await r.read()
                )
        else:
            new_guild = await self.bot.create_guild(name=ctx.guild.name)
#         await m.edit(
#             content="""
# :white_check_mark: - создан сервер
# :hourglass: - удаление всех каналов и ролей с сервера
# :x: - созданы каналы
# :x: - созданы роли
# :х: - полностью создан сервер
#         """
#         )
#         await m.edit(
#             content="""
# :white_check_mark: - создан сервер
# :white_check_mark: - удалены все каналы и роли с сервера
# :hourglass: - создание ролей
# :x: - созданы каналы
# :х: - полностью создан сервер
#         """
#         )
        roles = {}
        r = ctx.guild.roles
        r.reverse()
        for role in r:
            if (
                role.is_bot_managed()
                or role.is_default()
                or role.is_integration()
                or role.is_premium_subscriber()
            ):
                continue
            new_role = await new_guild.create_role(
                name=role.name,
                permissions=role.permissions,
                color=role.color,
                hoist=role.hoist,
                mentionable=role.mentionable,
            )
            roles[role] = new_role
        everyone = ctx.guild.default_role
        roles[everyone] = new_guild.default_role
        await new_guild.default_role.edit(
            permissions=everyone.permissions,
            color=everyone.color,
            hoist=everyone.hoist,
            mentionable=everyone.mentionable,
        )
        for dc in await new_guild.fetch_channels():
            await dc.delete()
#         await m.edit(
#             content="""
# :white_check_mark: - создан сервер
# :white_check_mark: - удалены все каналы и роли с сервера
# :white_check_mark: - созданы роли
# :hourglass: - создание каналов
# :х: - полностью создан сервер
#                 """
#         )
        channels = {None: None}
        for cat in ctx.guild.categories:
            new_c = await new_guild.create_category(
                name=cat.name, position=cat.position
            )
            channels[cat] = new_c
        for category in ctx.guild.by_category():
            catgroup = category[0]
            cat_channels = category[1]
            if catgroup:
                for c in cat_channels:
                    if isinstance(c, TextChannel):
                        # if c.type == ChannelType.text:
                        new_c = await new_guild.create_text_channel(
                            name=c.name,
                            category=channels[c.category],
                            position=c.position,
                            topic=c.topic,
                            slowmode_delay=c.slowmode_delay,
                            nsfw=c.nsfw,
                        )
                    # elif c.type == ChannelType.voice:
                    elif isinstance(c, VoiceChannel):
                        new_c = await new_guild.create_voice_channel(
                            name=c.name,
                            category=channels[c.category],
                            position=c.position,
                            user_limit=c.user_limit,
                        )
                    # elif c.type == ChannelType.news:
                    elif (
                        c.type == ChannelType.news
                    ):  # discord.py-self hasn't NewsChannel function
                        new_c = await new_guild.create_text_channel(
                            name=c.name,
                            category=channels[c.category],
                            position=c.position,
                            topic=c.topic,
                            slowmode_delay=c.slowmode_delay,
                            nsfw=c.nsfw,
                        )
                    channels[c] = new_c
            else:
                for c in cat_channels:
                    if isinstance(c, TextChannel):
                        new_c = await new_guild.create_text_channel(
                            name=c.name,
                            category=None,
                            position=c.position,
                            topic=c.topic,
                            slowmode_delay=c.slowmode_delay,
                            nsfw=c.nsfw,
                        )
                    elif isinstance(c, VoiceChannel):
                        new_c = await new_guild.create_voice_channel(
                            name=c.name,
                            category=None,
                            position=c.position,
                            user_limit=c.user_limit,
                        )
                    elif c.type == ChannelType.news:
                        new_c = await new_guild.create_text_channel(
                            name=c.name,
                            category=None,
                            position=c.position,
                            topic=c.topic,
                            slowmode_delay=c.slowmode_delay,
                            nsfw=c.nsfw,
                        )
                    channels[c] = new_c
        for c in ctx.guild.channels:
            # overs = c.overwrites
            over_new = {}
            for target, over in c.overwrites.items():
                if isinstance(target, Role):
                    try:
                        over_new[roles[target]] = over
                    except:
                        continue
            await channels[c].edit(overwrites=over_new)
#         await m.edit(
#             content="""
# :white_check_mark: - создан сервер
# :white_check_mark: - удалены все каналы и роли с сервера
# :white_check_mark: - созданы роли
# :white_check_mark: - созданы каналы
# :hourglass: - конец настройки сервера...
#                 """
#         )
        await new_guild.edit(
            verification_level=ctx.guild.verification_level,
            default_notifications=ctx.guild.default_notifications,
            explicit_content_filter=ctx.guild.explicit_content_filter,
            system_channel=channels[ctx.guild.system_channel],
            system_channel_flags=ctx.guild.system_channel_flags,
            afk_channel=channels[ctx.guild.afk_channel],
            afk_timeout=ctx.guild.afk_timeout,
            rules_channel=channels[ctx.guild.rules_channel] if ctx.guild.rules_channel else None,
            premium_progress_bar_enabled=ctx.guild.premium_progress_bar_enabled,
        )
        for emoji in ctx.guild.emojis:
            try:
                url = f'https://cdn.discordapp.com/emojis/{emoji.id}.{"gif" if emoji.animated else "png"}'
                async with request("GET", url) as emoji:
                    await new_guild.create_custom_emoji(
                        name=emoji.name, image=await emoji.read()
                    )
            except:
                continue
#         await m.edit(
#             content="""
# :white_check_mark: - создан сервер
# :white_check_mark: - удалены все каналы и роли с сервера
# :white_check_mark: - созданы роли
# :white_check_mark: - созданы каналы
# :white_check_mark: - полностью создан сервер
#                 """
#         )


def setup(bot):
    bot.add_cog(Cloner(bot))
