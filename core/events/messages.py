from os import getcwd, listdir, path
import os
from discord.ext import commands


class Messages(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot
        self.dir = getcwd()
    
    def check(self, ch, message, filenames: list):
        pathg = self.dir + '\\temp\\' + str(message.guild.id)
        if ch:
            print(f"""
DELETED MESSAGE + PHOTO(s)

guild: {message.guild} (id: {message.guild.id})
author: {message.author} (id: {message.author.id})
channel: {message.channel} ({message.channel.name} id: {message.channel.id})
content: {ch}
attachments: {", ".join([filename for filename in filenames])}
alt-text: {", ".join([desc.description for desc in message.attachments if desc.description])}
NOTE: all attachments saved in {pathg}""")
        else:
            print(f"""
DELETED MESSAGE + PHOTO(s)

guild: {message.guild} (id: {message.guild.id})
author: {message.author} (id: {message.author.id})
channel: {message.channel} ({message.channel.name} id: {message.channel.id})
attachments: {", ".join([filename for filename in filenames])}
alt-text: {", ".join([desc.description for desc in message.attachments if desc.description])}
NOTE: all attachments saved in {pathg}""")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """
        Messages delete
        """
        print(
f"""
EDITED MESSAGE

author: {after.author}
guild: {before.guild}
old message: {before.content}
channel: {before.channel}

new message: {after.content}
edited: {before.edited_at}
ID: {before.id}
url: {before.jump_url}
"""
        )
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.attachments:
            filenames = list()
            if path.exists(path.join(self.dir, 'temp', str(message.guild.id))):
                for attach in message.attachments:
                    os.chdir(path.join(self.dir + "\\temp\\" + str(message.guild.id)))
                    await attach.save(attach.filename)
                    filenames.append(attach.filename)
                self.check(message.content, message, filenames)
            else:
                os.chdir(path.join(self.dir + "\\temp\\"))
                os.mkdir(str(message.guild.id))
                for attach in message.attachments:
                    await attach.save(attach.filename)
                    filenames.append(attach.filename)
                self.check(message.content, message, filenames)
        else:
            print(f"""
DELETED MESSAGE

guild: {message.guild} (id: {message.guild.id})
author: {message.author} (id: {message.author.id})
content: {message.content}
channel: {message.channel} ({message.channel.name} id: {message.channel.id})""")

def setup(bot) -> None:
    bot.add_cog(Messages(bot))
