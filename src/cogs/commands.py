#region Imports
import os, json, discord, yaml

from discord.ext import commands
from utils import default
#endregion

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        with open(f'{os.getcwd()}/src/content.yml') as f:
            self.content = yaml.full_load(f)

    """ Starts the application process for a given user. """
    @commands.command(name='apply')
    async def apply(self, ctx):
        answers = []
        user = ctx.author

        def check(m):
            return m.author == user and not m.guild 

        for idx, question in enumerate(self.content['questions']):
            await self.dm(user, msg=f"Question #{idx + 1}: {question}")
            response = await self.bot.wait_for('message', check=check)
            answers.append(response.content)

        
        embed=discord.Embed(title="Oversight", color=0xFF5733)
        for (idx, question), answer in zip(enumerate(self.content['questions']), answers): 
            embed.add_field(name=f"Question #{idx + 1}: {question}", value=f"Response #{idx + 1}: {answer}", inline=False)
        embed.set_footer(text="Please check to make sure your responses are what you want")
        await user.send(embed=embed)    

    async def dm(self, user, msg=None):
        msg = msg or "Error, message was empty."
        await user.send(msg) 

def setup(bot):
    bot.add_cog(Commands(bot))
    