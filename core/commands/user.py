from discord.ext import commands


class User(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot
        self.badges = {
            # 0: "No Badge",
            1: "Discord Employee",
            2: "https://cdn.discordapp.com/emojis/934859467634409523.png?v=1&size=48",
            4: "https://cdn.discordapp.com/emojis/948557483595694120.gif?v=1&size=48",
            8: "https://cdn.discordapp.com/emojis/934859721628860527.png?v=1&size=48",
            16: "SMS recovery for 2FA enabled",
            32: "Dismissed Nitro promotion",
            64: "https://cdn.discordapp.com/emojis/934859971156385823.png?v=1&size=48",
            128: "https://cdn.discordapp.com/emojis/934859951938105435.png?v=1&size=48",
            256: "https://cdn.discordapp.com/emojis/934859988583731291.png?v=1&size=48",
            512: "https://cdn.discordapp.com/emojis/934859803241615460.png?v=1&size=48",
            1024: "Team User",
            2048: "Relates to partner/verification applications.",
            4096: "System User",
            8192: "Has an unread system message",
            16384: "https://cdn.discordapp.com/emojis/934859699080290314.png?v=1&size=48",
            32768: "Pending deletion for being underage in DOB prompt",
            65536: "Verified Bot",
            131072: "https://cdn.discordapp.com/emojis/934859626049073220.png?v=1&size=48",
            262144: "https://cdn.discordapp.com/emojis/934859591253119046.png?v=1&size=48",
            524288: "Bot has set an interactions endpoint url",
            1048576: "User is disabled for being a spammer",
        }
    @commands.command()
    async def user(self, ctx, user):
        if user:
            user_badges = []
            user = await commands.UserConverter().convert(ctx, user)
            # for pub in user.public_flags.value:
            #     print(pub)
            for a, b in self.badges.items():
                if user.public_flags._has_flag(a):
                    user_badges.append(b)
                    # print(f"User has {self.badges[a]} badge")
            # print(user.public_flags._has_flag())
            await ctx.reply(f"""
Информация о пользователе: {user}

Аватар: {user.avatar.url if user.avatar else 'Нет аватарки'}
Баннер: {user.banner.url if user.banner else 'Нет баннера'}
Бот? {'Да' if user.bot else 'Нет'}
Создан: {user.created_at.strftime("%d.%m.%Y %H:%M:%S")}
Друг? {'Да' if user.is_friend() else 'Нет'}
Заблокирован? {'Да' if user.is_blocked() else 'Нет'}
Флаги: {", ".join([badge for badge in user_badges])}
            """)

def setup(bot) -> None:
    bot.add_cog(User(bot))
