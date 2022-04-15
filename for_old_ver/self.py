from json import load, dump
from platform import python_version
from discord import __version__
from discord.ext import commands
from os import _exit, getcwd, listdir, system, name

cwd = getcwd()

def get_prefix(bot, message):
    with open(f"{cwd}\\config.json", "r") as j:
        config = load(j)
    if config["prefix"]:
        return commands.when_mentioned_or(config["prefix"])(bot, message)
    else:
        new()
        return commands.when_mentioned_or("@")(bot, message)


bot = commands.Bot(command_prefix=get_prefix, user_bot=True)


def new():
    token = input("Enter a token: ")
    q = input("Do you want write logs when member is joined/leaved to guild? (y/n): ")
    q2 = input("Do you want enable nitro sniper? (y/n)").lower()
    prefix = input(
        f"Enter a prefix for self (prefix can change with command `prefix`prefix change_prefix 'new prefix')"
    )
    if q == "y" or q == "n" and q2 == "y" or q2 == "n" and prefix:
        data = {
            "token": token,
            "write": q,
            "nitro_sniper": True if q2 == "y" else False,
            "prefix": prefix,
        }
        dump(data, open("config.json", "w"), indent=4)
        print("restarting...")
        system("python3 self.py" if name != "nt" else "python self.py")
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
    if bot.is_ready():
        print("Work!")

@bot.command()
async def reload(ctx, extension, event: bool = True):
    if extension:
        if event:
            bot.reload_extension(f"core.events.{extension}")
        else:
            bot.reload_extension(f"core.commands.{extension}")

if __name__ == "__main__":
    try:
        with open("config.json", "r") as j:
            config = load(j)
        if config["token"]:
            bot.run(config["token"])
        else:
            new()
    except FileNotFoundError:
        print("Create config.json file please")
