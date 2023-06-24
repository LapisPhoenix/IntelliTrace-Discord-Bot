import os
import json
import string
import discord
import aiohttp
from discord import app_commands
from discord.ext import commands

class Phone(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api_key = os.getenv("VERIPHONE")
    

    @app_commands.command(name="phonenumber", description="Verify a phone number and get general information about it.")
    async def phonenumber(self, interaction: discord.Interaction, phone_number: str):
        await interaction.response.defer(ephemeral=True, thinking=True)
        final_phone_number = ""

        for num in phone_number:
            if num in string.digits:
                final_phone_number += num

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.veriphone.io/v2/verify?phone={final_phone_number}&key={self.api_key}") as response:
                if response.status != 200:
                    await interaction.followup.send("An unknown error occurred!")
                    return
                
                data = await response.json()
                phone = data.get("phone")
                phone_valid = data.get("phone_valid")
                phone_type = data.get("phone_type")
                phone_region = data.get("phone_region")
                country = data.get("country")
                country_code = data.get("country_code")
                country_prefix = data.get("country_prefix")
                international_number = data.get("international_number")
                local_number = data.get("local_number")
                e164 = data.get("e164")
                carrier = data.get("carrier")

        embed2 = discord.Embed(title="Phone Information", description=f"Information about {phone_number}")
        embed2.add_field(name="Phone Number", value=phone, inline=False)
        embed2.add_field(name="Valid Phone Number", value=phone_valid, inline=False)
        embed2.add_field(name="Phone Type", value=phone_type.replace("_", " ").title(), inline=False)
        embed2.add_field(name="Phone Region", value=phone_region, inline=False)
        embed2.add_field(name="Country", value=country, inline=False)
        embed2.add_field(name="Country Code", value=country_code, inline=False)
        embed2.add_field(name="International Number", value=international_number, inline=False)
        embed2.add_field(name="Local Number", value=local_number)
        embed2.add_field(name="E614", value=e164)
        embed2.add_field(name="Carrier", value=carrier if carrier else "Unknown")

        await interaction.followup.send(embed=embed2, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Phone(bot))