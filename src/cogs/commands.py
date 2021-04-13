#region Imports
import os, json, discord, yaml, dotenv

from discord.ext import commands
from discord.utils import get
from utils import default
from utils.objects import Embed
#endregion

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        dotenv.load_dotenv()
        self.application_channel = os.getenv('APPLICATION_CHANNEL')

        with open(f'{os.getcwd()}/src/content.yml') as f:
            self.content = yaml.full_load(f)

    """ Starts the application process for a given user. """
    @commands.command(name='apply')
    async def apply(self, ctx):
        satisfied = False

        """ Asks the user the questions in content.yml through thier direct messages, and allows them to reanswer until satisfaction """
        while not satisfied:
            answers = []

            for idx, question in enumerate(self.content['questions']):
                await ctx.author.send(f'__#{idx + 1}: {question}__')
                response = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and not m.guild)
                answers.append(response.content)

            embed = Embed(bot=self.bot, title='Oversight', color=0xFF5733)
            for (idx, question), answer in zip(enumerate(self.content['questions']), answers): 
                embed.add_field(name=f'#{idx + 1}: {question}', value=f'*{answer}*', inline=False)
            
            await ctx.author.send(embed=embed)   
            await ctx.author.send(f'Are these answers correct? **(y/n)**')

            satisfied = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and not m.guild and (m.content == 'y' or m.content =='n'))

        await ctx.author.send('Your application is being processed, please be patient.')
        await self.send_to_applications(ctx.author, answers)

        """ Sends the user's application to the application channel. """
        # Reuse previous embed
        embed.title = f'{ctx.author}\'s Application'
        application_channel = get(ctx.guild.channels, name=self.application_channel)
        await application_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Commands(bot))
    