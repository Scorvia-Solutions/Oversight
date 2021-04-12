#region Imports
import os, json, discord, yaml, dotenv

from discord.ext import commands
from utils import default
from utils.objects import Embed
#endregion

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        with open(f'{os.getcwd()}/src/content.yml') as f:
            self.content = yaml.full_load(f)

    """ Starts the application process for a given user. """
    @commands.command(name='apply')
    async def apply(self, ctx):
        satisfied = False
        while not satisfied:
            response, answers = await self.ask_questions(ctx)
            satisfied = response

        await ctx.author.message('Your application is being processed, please be patient.')
        await self.send_to_applications(ctx.author, answers)

    async def send_to_applications(self, user, answers):
        pass
        
    """ Asks the user the questions in content.yml through thier direct messages, returns if they like their answers, and an array containing their answers. """
    async def ask_questions(self, ctx):
        answers = []

        for idx, question in enumerate(self.content['questions']):
            await self.dm(ctx.author, msg=f'__#{idx + 1}: {question}__')
            response = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and not m.guild)
            answers.append(response.content)

        embed=Embed(bot=self.bot, title='Oversight', color=0xFF5733)
        for (idx, question), answer in zip(enumerate(self.content['questions']), answers): 
            embed.add_field(name=f'#{idx + 1}: {question}', value=f'*{answer}*', inline=False)
        
        await ctx.author.send(embed=embed)   
        await ctx.author.send(f'Are these answers correct? **(y/n)**')

        return (await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and not m.guild and (m.content == 'y' or m.content =='n')), answers)

    """ Sends the message as a direct message to the user. """
    async def dm(self, user, msg=None):
        msg = msg or 'Error, message was empty.'
        await user.send(msg) 

def setup(bot):
    bot.add_cog(Commands(bot))
    