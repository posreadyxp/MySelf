from json import load, dump
from platform import python_version
from discord import __version__
from discord.ext import commands
from os import _exit, listdir, system, name

bot = commands.Bot(command_prefix="@", help_command=None, self_bot=True)


def new():
    token = input("Enter a token: ")
    q = input("Do you want write logs when member is joined/leaved to guild? (y/n): ")
    if q == "y" or q == "n":
        data = {"token": token, "write": q}
        dump(data, open("config.json", "w"))
        print("restarting...")
        system("python3 self.py") if name != "nt" else system("python self.py")
        _exit(0)
    else:
        return "Error"


# EVENT READY
@bot.event
async def on_connect():
    print(
        f"""
SELF BOT V0.1
BY POSREADY
PYTHON {python_version()}
DISCORD.PY SELF V{__version__}
    """
    )
    for event in listdir("core/events"):
        if event.endswith(".py"):
            bot.load_extension(f"core.events.{event[:-3]}")
            print(event[:-3], "Loaded!")
    for command in listdir("core/commands"):
        if command.endswith(".py"):
            bot.load_extension(f"core.commands.{command[:-3]}")
            print(command[:-3], "Loaded!")


try:
    with open("config.json", "r") as config:
        config = load(config)
        if config["token"]:
            bot.run(config["token"])
        else:
            new()
except FileNotFoundError:
    print("Create config.json file please")
