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
        self.server_ip = os.getenv('SERVER_IP')
        self.server_port = os.getenv('SERVER_PORT')
        self.rcon_password = os.getenv('RCON_PASSWORD')

        with open(f'{os.getcwd()}/src/content.yml') as f:
            self.content = yaml.full_load(f)

    """ Starts the application process for a given user. """
    @commands.command(name='apply')
    async def apply(self, ctx):
        satisfied = False

        if not ctx.guild:
            return # create a better method to notify user that the command must be invoked in a server, not dm, or make commands only function in servers

        """ Asks the user the questions in content.yml through their direct messages, and allows them to re-answer until satisfaction """
        while not satisfied:
            answers = []

            for idx, question in enumerate(self.content['questions']):

                question_embed = Embed(bot=self.bot, title=f'__Question #{idx + 1}:__', description=f'    *{question}*', color=0xFF5733)
                # questionEmbed.add_field(name=f'__Question #{idx + 1}:__', value=f'    *{question}*', inline=False)
                await ctx.author.send(embed=question_embed)
                
                response = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and not m.guild)
                answers.append(response.content)

            answer_embed = Embed(bot=self.bot, title='Oversight', color=0xFF5733)
            for (idx, question), answer in zip(enumerate(self.content['questions']), answers): 
                answer_embed.add_field(name=f'#{idx + 1}: {question}', value=f'    *{answer}*', inline=False)
            
            await ctx.author.send(embed=answer_embed)   
            await ctx.author.send(f'Are these answers correct? **(y/n)**')

            message = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and not m.guild and (m.content == 'y' or m.content =='n' or m.content == 'yes' or m.content == 'no'))
            satisfied = message.content == 'y' or message.content == 'yes'

        await ctx.author.send(self.content['responses']['pending']) # sends message saying your response is pending review

        """ Sends the user's application to the application channel. """
        # Reuse previous embed
        answer_embed.title = f'{ctx.author}\'s Application'
        application_channel = get(ctx.guild.channels, name=self.application_channel)
        
        application = await application_channel.send(embed=answer_embed)
        await application.add_reaction('\u2705')
        await application.add_reaction('\u274c')
            
        reaction, _ = await self.bot.wait_for('reaction_add', check=lambda r, u: u != self.bot.user and (r.emoji == '\u2705' or r.emoji == '\u274c'))
        accepted = True if reaction.emoji == '\u2705' else False

        if accepted:
            await ctx.author.send(self.content['responses']['accepted'])
            user = answers[-1]
            client = Client(self.server_ip, self.server_port, self.rcon_password)
            await client.connect()
            await client.send_cmd(f'whitelist {user}')
            await client.close()
        else:
            """ Application rejected, ? """

            await ctx.author.send(self.content['responses']['rejected']) 

        





def setup(bot):
    bot.add_cog(Commands(bot))
    
