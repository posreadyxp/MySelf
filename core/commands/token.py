import io
import discord
from discord.ext import commands
from aiohttp import ClientSession, request


class Token(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot
        self.statuses = [200, 204, 429, 201]

    @commands.group(name="token")
    async def token(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(
                """
```
! - обязательно

Доступные аргументы

token info !token
```
            """
            )

    # @token.command(name="info")
    # async def token_info(self, ctx, token):
    #     if token:
    #         m = await ctx.send("Ожидайте...")
    #         session = ClientSession()
    #         async with session.get()

    @token.command(name="checker")
    async def token_checker(self, ctx, token):
        if token:
            m = await ctx.reply("Ожидайте")
            async with request(
                "GET",
                "https://canary.discordapp.com/api/v9/users/@me",
                headers={"Authorization": token},
            ) as r:
                if r.status == 403:
                    await m.edit(content="Токен валидный, но фонлок")
                elif r.status == 401:
                    await m.edit(content="Токен инвалид")
                else:
                    async with request(
                        "GET",
                        "https://canary.discordapp.com/api/users/@me/guilds",
                        headers={"Authorization": token},
                    ) as r:
                        if (
                            "You need to verify your account in order to perform this action."
                            in await r.text()
                        ):
                            await m.edit(content="Токен валид, но просит верификацию")
                        else:
                            await m.edit(content="Токен валид")
                    # await m.edit(content="Токен валид")
                # if r.status == 403:
                #     await m.edit(content="Токен валидный, но фонлок")
                # elif r.status == 401:
                #     await m.edit(content="Токен инвалид")
                # else:
                #     await m.edit(content="Токен валид")

    @token.command(name="mass_checker")
    async def token_mass_checker(self, ctx, *, tokens):
        if tokens:
            tokens = tokens.split(" ")
            print(tokens)
            valids = list()
            invalids = list()
            phonelocks = list()
            m = await ctx.reply("Ожидайте")
            for token in tokens:
                async with request(
                    "GET",
                    "https://canary.discordapp.com/api/v9/users/@me",
                    headers={"Authorization": token},
                ) as r:
                    if r.status == 403:
                        phonelocks.append(token)
                    elif r.status == 401:
                        invalids.append(token)
                    else:
                        valids.append(token)
            await ctx.send(
                f"""
```
Информация о токенах

валидов: {len(valids)}
инвалидов: {len(invalids)}
фонлоков: {len(phonelocks)+1 if len(phonelocks) != 0 else len(phonelocks)}

токена ниже
```
            """,
                files=[
                    discord.File(
                        fp=io.StringIO("\n".join([valid for valid in valids])),
                        filename="valid.txt",
                    ),
                    discord.File(
                        fp=io.StringIO("\n".join([invalid for invalid in invalids])),
                        filename="invalid.txt",
                    ),
                    discord.File(
                        fp=io.StringIO(
                            "\n".join([phonelock for phonelock in phonelocks])
                        ),
                        filename="phonelock.txt",
                    ),
                ],
            )

    @token.command(name="checker_bot")
    async def token_checker_bot(self, ctx, token):
        if token:
            m = await ctx.reply("Ожидайте")
            session = ClientSession()
            async with session.get(
                "https://discord.com/api/v9/users/@me",
                headers={"Authorization": "Bot " + token},
            ) as r:
                if r.status == 403:
                    await m.edit(content="Токен валидный, но фонлок")
                elif r.status == 401:
                    await m.edit(content="Токен инвалид")
                else:
                    await m.edit(content="Токен валид")
                await session.close()

    @commands.command(alias=["webhook info"])
    async def webhook_info(self, ctx, webhook: str):
        if webhook:
            await ctx.message.delete()
            m = await ctx.send("Ожидайте")
            # webhook_status = request("GET", webhook)
            async with request("GET", webhook) as r:
                json = await r.json()
                if r.status == 200:
                    token = json["token"]
                    await m.edit(
                        content=f"""
```
Вебхук {webhook.replace(webhook.split("_")[1], "**********")} валид

INFO:

ID: {json["id"]}
Имя: {json["name"]}
channel ID: {json["id"]}
guild ID: {json["guild_id"]}
token: {token.replace(json["token"].split("_")[1], "**********")}
```
                    """
                    )
                else:
                    return await ctx.send(f"Вебхук {webhook} инвалид")

    @token.command(name="info")
    async def token_info(self, ctx, token):
        try:
            await ctx.message.delete()
        except:
            pass
        if token:
            m = await ctx.send("Ожидайте")
            async with request(
                "GET",
                "https://discord.com/api/v9/users/@me/guilds",
                headers={"Authorization": token},
            ) as r:
                if r.status == 403:
                    return await m.edit(content="Токен валидный, но фонлок")
                elif r.status == 401:
                    return await m.edit(content="Токен инвалид")
                else:
                    await m.edit(content="Токен валид")
            async with request(
                "GET",
                "https://canary.discordapp.com/api/v9/users/@me",
                headers={"Authorization": token},
            ) as r:
                if r.status in self.statuses:
                    json = await r.json()
                    ID = json["id"]
                    username = f"{json['username']}#{json['discriminator']}"
                    if json["avatar"]:
                        avatar = (
                            f'https://cdn.discordapp.com/avatars/{ID}/{json["avatar"]}.gif'
                            if json["avatar"].startswith("a_")
                            else f"https://cdn.discordapp.com/avatars/{ID}/{json['avatar']}.png"
                        )
                    else:
                        avatar = "по умолчанию"
                    if json["banner"]:
                        banner = (
                            f'https://cdn.discordapp.com/banners/{ID}/{json["banner"]}.gif'
                            if json["banner"].startswith("a_")
                            else f"https://cdn.discordapp.com/banners/{ID}/{json['banner']}.png"
                        )
                    else:
                        banner = "по умолчанию"
                    bio = json["bio"] if json["bio"] else "Нет био"
                    locale = json["locale"]
                    nsfw_allow = json["nsfw_allowed"]
                    mfa_enable = json["mfa_enabled"]
                    verify = json["verified"]
                    email = json["email"]
                    phone = json["phone"] if json["phone"] else "не привязано"
                    await m.edit(
                        content=f"""
```
Информация о токене:

    Ник#тег: {username}
    ID: {ID}
    EMAIL: {email}
    Аватарка: {avatar}
    Баннер: {banner}
    Биография: {bio}
    Локализация: {locale}
    NSFW включен? {"Да" if nsfw_allow else 'Нет'}
    2FA включен? {"Да" if mfa_enable else 'Нет'}
    Верифицирован? {"Да" if verify else 'Нет'}
    Телефон: {phone}
```
                    """
                    )


def setup(bot) -> None:
    bot.add_cog(Token(bot))
