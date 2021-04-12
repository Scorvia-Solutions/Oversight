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
with open(f'{FILEPATH}/src/content.yml') as file: 
    config = yaml.full_load(file)


# Bot Related Code 
bot = commands.Bot(command_prefix='!') 

@bot.event  # Sends message to terminal once bot is ready
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'{bot.user} has loaded up Modules!')

    game = discord.Game("Oversight v0.1")
    await bot.change_presence(status=discord.Status.online, activity=game)


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

    
async def dm(user, msg=None):
    msg = msg or "Error, message was empty."
    await user.send(msg) 



@bot.command()
async def info(ctx):
    await ctx.send(type.ctx.channel.type) 

@bot.command()
async def embed(ctx):
    embed=discord.Embed(title="Oversight", color=0xFF5733)
    embed.set_author(name="Scorvia Solutions", url="https://github.com/Scorvia-Solutions", icon_url="https://cdn.discordapp.com/attachments/797513405719117834/830220000601178162/oversight.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/797513405719117834/830220000601178162/oversight.png")
    embed.set_footer(text="Oversight v0.1 is maintained by Scorvia Solutions. Please contact WarpWing#3866 for any questions or concerns regarding Oversight.")
    embed.add_field(name="Response Verfication", value="Here are the responses to the application. Please check them over and make sure everything is properly submitted", inline=False) 
    embed.add_field(name="Question #1", value="This would be Response #1", inline=False)
    embed.add_field(name="Question #2", value="This would be Response #2", inline=False)
    embed.add_field(name="Question #3", value="This would be Response #3", inline=False)
    embed.add_field(name="Question #4", value="This would be Response #4", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def question(ctx):
    embed=discord.Embed(color=0xFF5733)
    embed.set_author(name="Oversight", icon_url="https://cdn.discordapp.com/attachments/797513405719117834/830220000601178162/oversight.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/797513405719117834/830220000601178162/oversight.png")
    embed.add_field(name="Question #1", value="How did you hear about our server?", inline=False)
    embed.set_footer(text="Please make sure to answer the question as best you can!")
    await ctx.send(embed=embed)

bot.run(f'{TOKEN}')
