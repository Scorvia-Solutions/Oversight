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


# Startup process
load_dotenv() # Loads Enviromental Secretsanswers = []
# Variables 
TOKEN = os.getenv('DISCORD_TOKEN')
FILEPATH = os.getcwd()
# Load Config File
with open(f'{FILEPATH}/src/config.yml') as file: 
    config = yaml.full_load(file)


# Bot Related Code 
bot = commands.Bot(command_prefix='!') 

@bot.event  # Sends message to terminal once bot is ready
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'{bot.user} has loaded up Modules!')

    game = discord.Game("Oversight v0.1")
    await bot.change_presence(status=discord.Status.online, activity=game)


# Register command(Will be removed)
@bot.command()
async def apply(ctx):
    answers = []
    user = ctx.author
    #channel = ctx.

    def check(m):
        return m.author == user and not m.guild 

    for idx, question in enumerate(config["questions"]):
        await dm(user, msg=f"Question #{idx + 1}: {question}")
        response = await bot.wait_for('message', check=check)
        answers.append(response.content)

    
# @client.event
# asnyc def on_message(message):
#     return await client.wait_for('message', check=check)

@bot.command()
async def info(ctx):
    await ctx.send(type.ctx.channel.type)
    
async def dm(user, msg=None):
    msg = msg or "Error, message was empty."
    await user.send(msg)

bot.run(f'{TOKEN}')
NEW
