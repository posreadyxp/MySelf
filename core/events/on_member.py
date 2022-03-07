from discord.ext import commands


class Member(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(
            f"""
NEW MEMBER JOINED!

Guild: {member.guild}
Acc: {member}
Activity: {member.activity}
Avatar: {member.avatar.url}:
    Animated? {member.avatar.is_animated()}
Banned: {member.banner.url}:
    Animated? {member.banner.is_animated()}
Bot? {member.bot}
Created: {member.created_at.strftime("%d.%m.%Y %H:%M:%S")}
Joined: {member.joined_at.strftime("%d.%m.%Y %H:%M:%S")}
Mobile? {member.is_on_mobile()}
Status: {member.raw_status}
Pending verification? {member.pending}
Your friend? {member.is_friend()} ({member.relationship.user if member.is_friend() else ''})
        """
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(
            f"""
NEW MEMBER LEAVED!

Guild: {member.guild}
Acc: {member}
Activity: {member.activity}
Avatar: {member.avatar.url}:
    Animated? {member.avatar.is_animated()}
Banned: {member.banner.url}:
    Animated? {member.banner.is_animated()}
Bot? {member.bot}
Created: {member.created_at.strftime("%d.%m.%Y %H:%M:%S")}
Joined: {member.joined_at.strftime("%d.%m.%Y %H:%M:%S")}
Mobile? {member.is_on_mobile()}
Status: {member.raw_status}
Pending verification? {member.pending}
Your friend? {member.is_friend()} ({member.relationship.user if member.is_friend() else ''})
        """
        )


def setup(bot) -> None:
    bot.add_cog(Member(bot))
