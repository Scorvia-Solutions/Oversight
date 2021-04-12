#region Imports
import os, dotenv

from utils import default
from utils.objects import Bot
#endregion

# config = default.get_json('config.json')
dotenv.load_dotenv()

token = os.getenv('DISCORD_TOKEN')

if token == None:
    raise Exception('No DISCORD_TOKEN found in .env')

bot = Bot(
    command_prefix  = '!',
    command_attrs   = dict(hidden=True)
)

print('Loading cogs...')

for file in os.listdir(f'{os.getcwd()}/src/cogs'):
    if file.endswith('.py'):
        print(f'--Loading \'{file}\'')
        name = file[:-3]
        bot.load_extension(f'cogs.{name}')

print('Cogs loaded, starting the bot...')

bot.run(token)
