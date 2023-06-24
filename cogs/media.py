import concurrent.futures
import io
import json
import os
import asyncio
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image, UnidentifiedImageError
from PIL.ExifTags import GPSTAGS, TAGS


class Media(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api_key = os.getenv("PASTEE")

    def create_google_maps_url(self, gps_coords):
        dec_deg_lat = self.convert_decimal_degrees(float(gps_coords["lat"][0]), float(gps_coords["lat"][1]), float(gps_coords["lat"][2]), gps_coords["lat_ref"])
        dec_deg_lon = self.convert_decimal_degrees(float(gps_coords["lon"][0]), float(gps_coords["lon"][1]), float(gps_coords["lon"][2]), gps_coords["lon_ref"])
        return f"https://maps.google.com/?q={dec_deg_lat},{dec_deg_lon}"

    def convert_decimal_degrees(self, degree, minutes, seconds, direction):
        decimal_degrees = degree + minutes / 60 + seconds / 3600
        if direction == "S" or direction == "W":
            decimal_degrees *= -1
        return decimal_degrees

    def open_image(self, content):
        return Image.open(io.BytesIO(content))

    def grab_exif_info(self, image):
        gps_info = ""
        other_info = ""
        gps_coords = {}

        if image._getexif() is None:
            return "No Exif Data Found!"

        for tag, value in image._getexif().items():
            tag_name = TAGS.get(tag)
            if tag_name == "GPSInfo":
                for key, val in value.items():
                    gps_info += f"{GPSTAGS.get(key)} - {val}\n"

                    if GPSTAGS.get(key) == "GPSLatitude":
                        gps_coords["lat"] = val
                    elif GPSTAGS.get(key) == "GPSLongitude":
                        gps_coords["lon"] = val
                    elif GPSTAGS.get(key) == "GPSLatitudeRef":
                        gps_coords["lat_ref"] = val
                    elif GPSTAGS.get(key) == "GPSLongitudeRef":
                        gps_coords["lon_ref"] = val
            else:
                other_info += f"{tag_name} - {value}\n"

        if gps_coords:
            google_map_url = self.create_google_maps_url(gps_coords)
        else:
            google_map_url = "No URL."

        return (gps_info, other_info, google_map_url)

    async def process_image(self, data):
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as exe:
            try:
                image = await loop.run_in_executor(exe, self.open_image, data)
                exif_info = await loop.run_in_executor(exe, self.grab_exif_info, image)
                return exif_info
            except UnidentifiedImageError:
                return "Invalid image file. Currently accepted formats: JPG, TIFF. You can also check if the image is corrupted."

    @app_commands.command(name="exif_data_extraction", description="Grab Exif from a direct image URL.")
    async def exif_data_extraction(self, interaction: discord.Interaction, url: str):
        await interaction.response.defer(ephemeral=True, thinking=True)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.read()

        exif_info = await self.process_image(data)

        if isinstance(exif_info, str):
            await interaction.followup.send(exif_info, ephemeral=True)
            return

        gps_info, other_info, google_map_url = exif_info

        final_string = f"""GPS\nGoogle Map: {google_map_url}\n{gps_info}\n------------\nOTHER\n{other_info}"""

        async with aiohttp.ClientSession() as session:
            url = f"https://api.paste.ee/v1/pastes/?key={self.api_key}"
            headers = {
                "Content-Type": "application/json",
                # "Authorization": f"Bearer {self.api_key}"
            }
            payload = {
                "sections":[
                    {"name":"Image Meta Data","syntax":"autodetect","contents":final_string}
                ]
            }

            async with session.post(url, headers=headers, json=payload) as response:
                resp = await response.text()
                jsonny = json.loads(resp)
                await interaction.followup.send(f"Here is your information!\n{jsonny['link']}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Media(bot))
