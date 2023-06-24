import discord
from discord import app_commands
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    

    @app_commands.command(name="ping", description="Gets the bot's latency.")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f":ping_pong: Latency: {round(self.bot.latency * 1000)}")
    

    @app_commands.command(name="legal", description="The legal terms of the bot.")
    async def legal(self, interaction: discord.Interaction):
        embed = discord.Embed(title="IMPORTANT", description="Before using the bot you ***MUST*** read the Terms Of Service and Privacy Policy!")
        embed.add_field(name="Terms Of Service", value="[Link Here](https://raw.githubusercontent.com/LapisPhoenix/OSINT-Discord-Bot/main/TERMS%20OF%20SERVICE)")
        embed.add_field(name="Privacy Policy", value="[Link Here](https://raw.githubusercontent.com/LapisPhoenix/OSINT-Discord-Bot/main/PRIVACY%20POLICY)")
        embed.set_footer(text="By Continuing to use the bot in any sort of compacity you agree to BOTH Terms of Service and Privacy Policy.")

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(General(bot))