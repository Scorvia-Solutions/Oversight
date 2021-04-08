import datetime
import dotenv
import sys
import os 
import json
import discord
import requests
from discord.ext import commands
import time

bot = commands.Bot(command_prefix='1')
bot.remove_command("help")

@bot.event  # Sends message to terminal once bot is ready
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'{bot.user} has loaded up Modules!')

    activity = discord.Game(name="Oversight v0.1", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)


bot.run('')

