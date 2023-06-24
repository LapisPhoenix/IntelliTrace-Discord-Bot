import discord
from difflib import get_close_matches
from discord import app_commands
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        channels = guild.text_channels
        embed = discord.Embed(title="IMPORTANT", description="Before using the bot you ***MUST*** read the Terms Of Service and Privacy Policy!")
        embed.add_field(name="Terms Of Service", value="[Link Here](https://raw.githubusercontent.com/LapisPhoenix/OSINT-Discord-Bot/main/TERMS%20OF%20SERVICE)")
        embed.add_field(name="Privacy Policy", value="[Link Here](https://raw.githubusercontent.com/LapisPhoenix/OSINT-Discord-Bot/main/PRIVACY%20POLICY)")
        embed.set_footer(text="By Continuing to use the bot in any sort of compacity you agree to BOTH Terms of Service and Privacy Policy.")

        # Find a channel, dont care which one.
        for channel in channels:
            try:
                await channel.send(embed=embed)
                break
            except discord.HTTPException:
                continue

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):   
        if isinstance(error, commands.CommandNotFound):
            user_input = ctx.message.content.split()[0][1:]  

            # Get all commands from the bot
            commands_list = [command.name for command in self.bot.commands]

            # Get the closest match
            closest_match = get_close_matches(user_input, commands_list, n=1, cutoff=0.6)

            if closest_match:
                suggestion = f"Command `{user_input}` not found. Did you mean `{closest_match[0]}`?"
                await ctx.send(suggestion)
            else:
                await ctx.send(f"Unknown Command! Run `{self.bot.command_prefix}help`!")
        else:
            await ctx.send("An error occured.")
            self.bot.log.log(self.bot.log.Level.ERROR, str(error))


async def setup(bot):
    await bot.add_cog(Events(bot))