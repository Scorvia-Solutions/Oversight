#region Imports
import os, json, discord, yaml, dotenv, asyncio
from aiomcrcon import Client

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
        self.serverip = os.getenv('SERVER_IP')
        self.serverport = os.getenv('SERVER_PORT')
        self.rconpass = os.getenv('RCON_PASSWORD')

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

            message = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and not m.guild and (m.content == 'y' or m.content =='n'))
            satisfied = message.content == 'y'

        await ctx.author.send(self.content['responses']['pending'])

        """ Sends the user's application to the application channel. """
        # Reuse previous embed
        embed.title = f'{ctx.author}\'s Application'
        application_channel = get(ctx.guild.channels, name=self.application_channel)
        
        application = await application_channel.send(embed=embed)
        await application.add_reaction('\u2705')
        await application.add_reaction('\u274c')
            
        reaction, _ = await self.bot.wait_for('reaction_add', check=lambda r, u: u != self.bot.user and (r.emoji == '\u2705' or r.emoji == '\u274c'))
        accepted = True if reaction.emoji == '\u2705' else False

        if accepted:
            await ctx.author.send(self.content['responses']['accepted'])
            user = answers[4]
            client = Client(self.serverip, self.serverport, self.rconpass)
            await client.connect()
            await client.send_cmd(f"whitelist {user}")
            await client.close()
        else:
            """ Application rejected, ? """

            await ctx.author.send(self.content['responses']['rejected']) 

        





def setup(bot):
    bot.add_cog(Commands(bot))
    