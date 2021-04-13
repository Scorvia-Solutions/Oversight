#region Imports
import discord

from discord.ext import commands
from discord.ext.commands import errors
#endregion

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    """  """
    @commands.Cog.listener()
    async def on_ready(self):
        print('\nSucessfully started and logged in.\n')

        game = discord.Game('Oversight v0.1')
        await self.bot.change_presence(status=discord.Status.online, activity=game)

    """ Generic error handler, will be changed later. """
    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, errors.MissingRequiredArgument) or isinstance(err, errors.BadArgument) or isinstance(err, errors.TooManyArguments):
            cmd = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(ctx.command)
            await ctx.send_help(cmd)

        elif isinstance(err, errors.CommandInvokeError):
            if '2000 or fewer' in str(err) and len(ctx.message.clean_content) > 1900:
                return await ctx.send('You attempted to make the command display more than 2,000 characters.\nBoth the error and the command will be ignored.')

            print(err)
            await ctx.send(f'There was an error processing the command. {error}')
        
        elif isinstance(err, errors.MaxConcurrencyReached):
            await ctx.send(f'You\'ve reached max capacity of command usage at once, please finish the previous one.')

        elif isinstance(err, errors.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown. Try again in {err.retry_after:.2f} seconds.')

        elif isinstance(err, errors.CheckFailure):
            pass

        elif isinstance(err, errors.CommandNotFound):
            pass

def setup(bot):
    bot.add_cog(Events(bot))