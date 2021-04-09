import datetime
import sys
import os 
import json
import discord
import requests
import time
import asyncio
import yaml
from discord.ext import commands
from dotenv import load_dotenv


#Startup functions
load_dotenv()
# Variables 
TOKEN = os.getenv('DISCORD_TOKEN')
FILEPATH = os.getcwd()
#Load Config File
with open(f'{FILEPATH}/src/config.yml') as file: 
    config = yaml.full_load(file)
 

# Bot Related Code 
bot = commands.Bot(command_prefix='!')
bot.remove_command("help")

@bot.event  # Sends message to terminal once bot is ready
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'{bot.user} has loaded up Modules!')

    activity = discord.Game(name="Oversight v0.1", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)

# Register command 
@bot.command()
async def form(ctx):
    await ctx.send(config)

bot.run(f'{TOKEN}')


