import os
import sys
import discord
import colorama
from log import Logger
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv

class BotClient(commands.Bot):
    def __init__(self, command_prefix, help_command, intents):
        super().__init__(command_prefix=None, help_command=help_command, intents=intents)
        self.log = Logger()

    async def on_ready(self):
        OSINT.clear_console()
        OSINT.div(title="commands")
        files = 0
        loaded_files = 0

        try:
            for file in os.listdir("./cogs"):
                if file.endswith(".py"):
                    files += 1
                    self.log.log(self.log.Level.INFO, f"Found {file}")
                    try:
                        await self.load_extension(f"cogs.{file[:-3]}")
                        loaded_files += 1
                    except Exception as e:
                        self.log.log(self.log.Level.ERROR, f"Failed to load \"cogs.{file[:-3]}\". (Error dumped in log file)")
                        self.log.dump_into_file(str(e))
        except FileNotFoundError:
            self.log.log(self.log.Level.FATAL, "Cogs folder not found!")
            await self.close()
            sys.exit(1)
        
        self.log.log(self.log.Level.INFO, "Syncing Commands For Slash Commands")
        try:
            synced = await self.tree.sync()
            failed_to_sync = (False, "Synced All Commands.")
        except Exception as e:
            failed_to_sync = (True, str(e))

        OSINT.div(title='status')
        bot_user = OSINT.colorize(str(self.user), colorama.Fore.LIGHTBLUE_EX)
        commands_loaded = OSINT.colorize(str(loaded_files), colorama.Fore.LIGHTBLUE_EX)
        servers = OSINT.colorize(str(len(self.guilds)), colorama.Fore.LIGHTBLUE_EX)
        prefix = OSINT.colorize(self.command_prefix, colorama.Fore.LIGHTBLUE_EX)
        good_status = OSINT.colorize("GOOD", colorama.Fore.GREEN)
        bad_status = OSINT.colorize("BAD", colorama.Fore.RED)
        status = ""
        diagnostic = ""

        if loaded_files >= files:
            status += good_status
            diagnostic += OSINT.colorize("No problems found.", colorama.Fore.GREEN)
        else:
            status += bad_status
            diagnostic += OSINT.colorize(f"Found {files} files in 'cogs' folder but loaded {loaded_files} files!", colorama.Fore.RED)
        
        if status == good_status and failed_to_sync[0] == True and failed_to_sync[1] != "Synced All Commands":
            status = bad_status
            diagnostic = OSINT.colorize(f"Failed to sync all slash commands. (Error dumped in log)", colorama.Fore.RED)
            self.log.dump_into_file(failed_to_sync[1])
        elif status == bad_status:
            diagnostic += OSINT.colorize(f"\n                 Failed to sync all slash Commands. (Error dumped in log)", colorama.Fore.RED)
            self.log.dump_into_file(failed_to_sync[1])
        else:
            diagnostic += OSINT.colorize(f"\n                 {failed_to_sync[1]}", colorama.Fore.GREEN)


        print(f"""Status:          {status}
Diagnostic:      {diagnostic}
Bot Name:        {bot_user}
Files Loaded:    {commands_loaded}
Guilds:          {servers}
Prefix:          {prefix}
""")

        OSINT.div(title="logs")


class OSINT:
    def __init__(self):
        self.bot = None
        self.log = Logger()

    def run(self):
        self.load_envs()
        TOKEN = os.getenv("TOKEN")
        self.bot = BotClient(command_prefix='$', help_command=None, intents=self.get_intents())
        self.bot.run(TOKEN)

    @staticmethod
    def get_intents():
        intents = discord.Intents.default()
        intents.messages = True
        intents.guilds = True
        intents.reactions = True
        intents.message_content = True
        intents.emojis = True
        intents.members = True
        return intents
    
    @staticmethod
    def clear_console():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def div(seperator: str = "-", title: str = None):
        if title is None:
            title = "PLACEHOLDER"

        if len(seperator) != 1:
            self.log.log(self.log.Level.WARNING, "Separator length must be 1 character long, defaulting to '-'")
            seperator = '-'

        title = title.upper()
        amount = 30

        if len(title) > amount:
            amount = len(title) + 2

        padding = (amount - len(title)) // 2
        padding_left = padding_right = padding

        if (amount - len(title)) % 2 != 0:
            padding_right += 1

        print(f"{seperator * padding_left} {title} {seperator * padding_right}")

    def load_envs(self):
        load_dotenv('.env')
        self.log.log(self.log.Level.SUCCESS, "Loaded environment variables")

    @staticmethod
    def colorize(text, color):
        return f"{color}{text}{colorama.Fore.RESET}"

if __name__ == "__main__":
    bot = OSINT()
    bot.run()
