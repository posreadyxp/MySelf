from datetime import datetime
import os
from re import search
from colorama import Fore, init
from discord.ext import commands
from json import load
from aiohttp import request


class Messages(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot
        self.dir = os.getcwd()
        init(autoreset=True)
        with open('config.json', 'r') as r:
            self.json = load(r)
        self.nitro_sniper = self.json["nitro_sniper"]
    
    def NitroData(self, message, elapsed, code):
        if message.guild:
            print(f"""
{Fore.WHITE} - Канал: {Fore.YELLOW}[{message.channel}] 
\n{Fore.WHITE} - Сервер: {Fore.YELLOW}[{message.guild}] ({message.guild.id})
\n{Fore.WHITE} - Автор: {Fore.YELLOW}[{message.author}]
\n{Fore.WHITE} - Заняло: {Fore.YELLOW}[{elapsed}]
\n{Fore.WHITE} - Код: {Fore.YELLOW}{code}
        """)
        else:
            print(f"""
{Fore.WHITE} - Код: {Fore.YELLOW}{code}
\n{Fore.WHITE} - Заняло: {Fore.YELLOW}[{elapsed}]
            """)

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
        # await after.
        await self.bot.process_commands(after)
        if before != after:
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
        if message:
            if message.attachments:
                filenames = list()
                if os.path.exists(os.path.join(self.dir, 'temp', str(message.guild.id))):
                    for attach in message.attachments:
                        os.chdir(os.path.join(self.dir + "\\temp\\" + str(message.guild.id)))
                        await attach.save(attach.filename)
                        filenames.append(attach.filename)
                    self.check(message.content, message, filenames)
                else:
                    os.chdir(os.path.join(self.dir + "\\temp\\"))
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

    @commands.Cog.listener()
    async def on_message(self, message):
        if 'discord.gift' in message.content or 'discord.com/gifts' in message.content:
            if self.nitro_sniper:
                start = datetime.now()
                code = search("discord.com/gifts/(.*)" if 'discord.com/gifts' in message.content else "discord.gift/(.*)", message.content)
                # print(code.group(1))# replace(".", "")
                token = self.json["token"]
                # info = request("POST", f'https://discordapp.com/api/v6/entitlements/gift-codes/{code}/redeem', headers={"Autorization": token})
                async with request("POST", f'https://discordapp.com/api/v9/entitlements/gift-codes/{code.group(1)}/redeem', headers={"Authorization": token}) as r:
                    info = await r.text()
                ex = datetime.now() - start
                ex = f'{ex.seconds}.{ex.microseconds}'

                if 'This gift has been redeemed already.' in info:
                    print(f"""
\n{Fore.CYAN}[{datetime.now()} - Похоже, кто-то быстрее вас забрал нитро..]
{self.NitroData(ex, code)}
                    """)

                elif 'subscription_plan' in info:
                    print(f"""
\n{Fore.CYAN}[{datetime.now()} - Успешно забрал нитро!]
{self.NitroData(ex, code)}
                    """)

                elif 'Unknown Gift Code' in info:
                    print(f"""
\n{Fore.CYAN}[{datetime.now()} - Не найден такой код]
{self.NitroData(ex, code)}
                    """)
                
                elif 'You are being rate limited.' in info:
                    print("Rate limit in account.")

def setup(bot) -> None:
    bot.add_cog(Messages(bot))
