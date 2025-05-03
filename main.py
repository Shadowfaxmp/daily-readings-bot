import asyncio

from discord.ext import tasks

from reading_scraper import fetch_daily_readings
import discord
import os
from dotenv import load_dotenv


async def send_message_to_channel(channel_id, message):
    """Send a message to the specified Discord channel."""
    channel = client.get_channel(channel_id)
    if channel is None:
        print(f"Channel with ID {channel_id} not found!")
        return
    await channel.send(message)


# Setup
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

    await asyncio.sleep(3) #Wait a few seconds because discord
    daily_readings_task.start()

@tasks.loop(hours=24)
async def daily_readings_task():

    channel_id = 1368029265269887078  # Your channel ID

    await client.wait_until_ready()  # Make sure client is connected

    readings = fetch_daily_readings()

    title_formatted = f"# {readings['title']}"
    await send_message_to_channel(channel_id, title_formatted)

    for section, content in readings.items():
        if content:
            message = f"## {section}\n\n{content}"
        else:
            message = f"# {section}\n\nSection not found or not available for this date."

        if content and section != 'title':
            await send_message_to_channel(channel_id, message)


client.run(TOKEN)